"""
Reddit thread JSON → Markdown converter.

Usage:
    1. Open each Reddit thread in your browser while logged in.
    2. Append `.json` to the URL (e.g. https://reddit.com/r/GNV/comments/abc/.json).
    3. Select all, copy, and paste into a file under docs-unclean/reddit-json/.
       Name each file after the thread slug (the last path segment of the URL):
           best_food_and_locations_in_gainesville_2025.json
           fun_hidden_gems_in_gnv_that_are_cheapfree.json
           ideas_for_fun_things_to_do_in_gainesville_that.json
    4. Run: python scrape_reddit.py
       Markdown files are written to docs-unclean/.
"""

import json
from pathlib import Path

JSON_DIR = Path("./docs-unclean/reddit-json")
OUTPUT_DIR = Path("./docs-unclean")

THREAD_META = {
    "best_food_and_locations_in_gainesville_2025": (
        "https://www.reddit.com/r/GNV/comments/1ldgqxr/best_food_and_locations_in_gainesville_2025/"
    ),
    "fun_hidden_gems_in_gnv_that_are_cheapfree": (
        "https://www.reddit.com/r/GNV/comments/171j93p/fun_hidden_gems_in_gnv_that_are_cheapfree/"
    ),
    "ideas_for_fun_things_to_do_in_gainesville_that": (
        "https://www.reddit.com/r/GNV/comments/1etmfsi/ideas_for_fun_things_to_do_in_gainesville_that/"
    ),
}


def extract_comments(children: list, depth: int = 0) -> list[str]:
    """Recursively extract comment bodies from a Reddit comment tree."""
    texts = []
    for child in children:
        if child.get("kind") == "more":
            continue
        data = child.get("data", {})
        body = data.get("body", "").strip()
        if body and body not in ("[deleted]", "[removed]"):
            prefix = "> " * depth
            texts.append(prefix + body)
        replies = data.get("replies")
        if isinstance(replies, dict):
            nested = replies.get("data", {}).get("children", [])
            texts.extend(extract_comments(nested, depth + 1))
    return texts


def json_to_markdown(slug: str, data: list) -> str:
    post_data = data[0]["data"]["children"][0]["data"]
    title = post_data.get("title", "").strip()
    selftext = post_data.get("selftext", "").strip()
    subreddit = post_data.get("subreddit_name_prefixed", "r/GNV")
    source_url = THREAD_META.get(slug, "")

    comment_children = data[1]["data"]["children"]
    comments = extract_comments(comment_children)

    lines = [
        f"# {title}",
        "",
        f"**Source:** {source_url}  ",
        f"**Subreddit:** {subreddit}",
        "",
    ]

    if selftext:
        lines += ["## Post", "", selftext, ""]

    if comments:
        lines += ["## Comments", ""]
        for comment in comments:
            lines.append(comment)
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def convert_thread(json_path: Path) -> None:
    slug = json_path.stem
    print(f"Processing: {json_path.name}")

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    markdown = json_to_markdown(slug, data)
    out_path = OUTPUT_DIR / f"{slug}.md"
    out_path.write_text(markdown, encoding="utf-8")
    print(f"  Saved {len(markdown):,} chars → {out_path.name}")


def main():
    if not JSON_DIR.exists():
        JSON_DIR.mkdir(parents=True)
        print(f"Created {JSON_DIR}/ — paste your Reddit JSON files here, then re-run.")
        return

    json_files = sorted(JSON_DIR.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {JSON_DIR}/. See the usage instructions at the top of this file.")
        return

    for json_path in json_files:
        convert_thread(json_path)

    print("Done.")


if __name__ == "__main__":
    main()
