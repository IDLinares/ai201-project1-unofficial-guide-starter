"""
TripAdvisor indoor activities parser for Gainesville, FL.

Reads the manually saved HTML from:
    docs-unclean/tripadvisor-html/attractions_activities_gainesville_florida.html

Extracts attraction name, rating, review count, category, and description,
then writes a markdown file to docs-unclean/tripadvisor-gainesville.md.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.tripadvisor.com/Attractions-g34242-Activities-zft11295-Gainesville_Florida.html"
INPUT_HTML = Path("./docs-unclean/tripadvisor-html/attractions_activities_gainesville_florida.html")
OUTPUT_FILE = Path("./docs-unclean/tripadvisor-gainesville.md")


def parse_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select('[data-automation="cardWrapper"]')

    lines = [
        "# Indoor Activities in Gainesville, FL",
        "",
        f"**Source:** {SOURCE_URL}  ",
        "**Platform:** TripAdvisor",
        "",
        "## Attractions",
        "",
    ]

    for card in cards:
        # Name lives in the h3; the rank number ("1.", "2.") is in a nested
        # span.vAUKO — remove it before reading the name text.
        name_el = card.select_one("h3")
        if not name_el:
            continue
        rank_span = name_el.select_one(".vAUKO")
        if rank_span:
            rank_span.decompose()
        name = name_el.get_text(strip=True)
        if not name:
            continue

        rating = ""
        rating_el = card.select_one('[data-automation="bubbleRatingValue"]')
        if rating_el:
            rating = rating_el.get_text(strip=True)

        reviews = ""
        reviews_el = card.select_one('[data-automation="bubbleReviewCount"]')
        if reviews_el:
            reviews = reviews_el.get_text(strip=True).strip("()")

        # Category text lives in a specific class inside .NxKBB.BKifx;
        # sibling divs hold the "Temporarily closed" badge — select only the text node.
        category = ""
        category_el = card.select_one(".NxKBB.BKifx .VImYz")
        if category_el:
            category = category_el.get_text(strip=True)

        status = ""
        status_el = card.select_one(".NxKBB.BKifx .bRMrl")
        if status_el:
            status = status_el.get_text(strip=True)

        description = ""
        desc_el = card.select_one('[data-automation="listCardDescription"]')
        if desc_el:
            raw = desc_el.get_text(separator=" ", strip=True)
            description = re.sub(r"\s+", " ", raw).strip()

        lines.append(f"### {name}")
        meta_parts = []
        if rating:
            meta_parts.append(f"Rating: {rating}/5")
        if reviews:
            meta_parts.append(f"{reviews} reviews")
        if category:
            meta_parts.append(category)
        if status:
            meta_parts.append(status)
        if meta_parts:
            lines.append(f"**{' | '.join(meta_parts)}**")
        if description:
            lines.append(f"\n{description}")
        lines.append("")

    return "\n".join(lines)


def main():
    if not INPUT_HTML.exists():
        print(f"HTML file not found: {INPUT_HTML}")
        return

    print(f"Parsing: {INPUT_HTML}")
    html = INPUT_HTML.read_text(encoding="utf-8")
    markdown = parse_html(html)

    OUTPUT_FILE.write_text(markdown, encoding="utf-8")
    print(f"Saved {len(markdown):,} chars -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
