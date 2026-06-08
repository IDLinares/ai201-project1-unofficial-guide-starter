"""
clean_docs.py — Clean all markdown files in docs-unclean/ and write to docs-clean/.

Operations applied to every file:
  1. Decode HTML entities  (&amp; → &, etc.)
  2. Remove boilerplate header lines  (date/category tags, author bylines)
  3. Strip inline link URLs  ([text](url) → text)
  4. Remove navigation-only lines  (Explore More, Read Next, Get the Guide, etc.)
  5. Remove promotional sections  (entire section when header contains CTA keywords)
  6. Remove promotional paragraphs  (paragraph contains explicit CTA signals)
  7. Remove duplicate page title  (H2 that mirrors the H1 at the top)
  8. Fix malformed headers  (strip stray ** from inside header lines)
  9. Remove orphaned short attribution lines  (e.g. "Wikipedia", "Florida Museum")
 10. Normalize whitespace  (collapse 3+ blank lines → 2, strip trailing spaces)
"""

import html
import re
from pathlib import Path

INPUT_DIR = Path("./docs-unclean")
OUTPUT_DIR = Path("./docs-clean")

# ── Constants ─────────────────────────────────────────────────────────────────

# Section-header substrings (lowercase) that flag an entire section for removal
CTA_SECTION_KEYWORDS = [
    "stay at",
    "make your trip",
    "fantastic place",
    "place to stay",
    "joy of day trips",
]

# Regex patterns searched in lowercase paragraph text; any match → drop paragraph
CTA_PARA_SIGNALS = [
    r"contact us today",
    r"schedule a tour",
    r"our leasing team",
    r"free vacation guide",
    r"looking for a new home",
    r"looking for a place to stay while visiting",
    r"book direct and save",
    r"can't wait to host you",
    r"we know you.re going to love it here",
    r"\(\d{3}\)\s*\d{3}[-.\s\d]{6,}",  # phone numbers e.g. (352) 268-1865
]

# Regex patterns for lines that are pure navigation text (run AFTER link stripping)
NAV_LINE_PATTERNS = [
    r"^read next:\s",
    r"^\*{0,2}explore more\s*>?\s*\*{0,2}$",
    r"^\*{0,2}learn more\s*>?\s*\*{0,2}$",
    r"^\*{0,2}read more\s*>?\s*\*{0,2}$",
    r"^\*{0,2}\*?get the guide\*?\*{0,2}$",
    r"^\*{0,2}\*?book now\*?\*{0,2}$",
    r"^\*{0,2}\*?book your stay\*?\*{0,2}$",
]


# ── Individual cleaning steps ─────────────────────────────────────────────────

def decode_html_entities(text: str) -> str:
    return html.unescape(text)


def remove_boilerplate_lines(text: str) -> str:
    """Drop date/category tag lines and author bylines."""
    result = []
    for line in text.split("\n"):
        s = line.strip()
        # "Mar 11, 2025 | [Assisted Living](...), ..."
        if re.match(r"^[A-Z][a-z]{2}\s+\d+,\s+\d{4}\s*\|", s):
            continue
        # "## By Firstname Lastname"
        if re.match(r"^#{1,3}\s+By\s+[A-Z]", s):
            continue
        result.append(line)
    return "\n".join(result)


def strip_link_urls(text: str) -> str:
    """[text](url) → text"""
    return re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)


def remove_nav_text_lines(text: str) -> str:
    """Remove lines that are pure navigation text (run after link stripping)."""
    result = []
    for line in text.split("\n"):
        s = line.strip()
        if any(re.match(p, s, re.IGNORECASE) for p in NAV_LINE_PATTERNS):
            continue
        result.append(line)
    return "\n".join(result)


def remove_cta_sections(text: str) -> str:
    """Remove entire sections whose headers signal promotional content."""
    lines = text.split("\n")
    result = []
    skipping = False
    skip_level = 0

    for line in lines:
        m = re.match(r"^(#{2,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            header_lower = m.group(2).lower()
            if any(kw in header_lower for kw in CTA_SECTION_KEYWORDS):
                skipping = True
                skip_level = level
                continue
            elif skipping and level <= skip_level:
                skipping = False
        if not skipping:
            result.append(line)

    return "\n".join(result)


def remove_cta_paragraphs(text: str) -> str:
    """Remove paragraphs that contain explicit promotional/CTA signals."""
    paragraphs = re.split(r"\n{2,}", text)
    kept = []
    for para in paragraphs:
        if any(re.search(sig, para.lower()) for sig in CTA_PARA_SIGNALS):
            continue
        kept.append(para)
    return "\n\n".join(kept)


def remove_duplicate_title(text: str) -> str:
    """Drop an H2 that duplicates (or extends) the H1 at the top of the file."""
    lines = text.split("\n")
    h1_text = None
    removed_dupe = False
    result = []

    for line in lines:
        if h1_text is None:
            m = re.match(r"^#\s+(.+)$", line)
            if m:
                h1_text = m.group(1).strip()

        if h1_text and not removed_dupe:
            m = re.match(r"^##\s+(.+)$", line)
            if m:
                h2_text = m.group(1).strip()
                # Normalize: strip parenthetical suffixes and compare
                h1_norm = re.sub(r"\s*\(.*?\)", "", h1_text).strip().lower()
                h2_norm = re.sub(r"\s*\(.*?\)", "", h2_text).strip().lower()
                if h1_norm in h2_norm or h2_norm in h1_norm:
                    removed_dupe = True
                    continue

        result.append(line)

    return "\n".join(result)


def fix_headers(text: str) -> str:
    """Strip stray ** markers and escaped asterisks from header lines."""
    def _clean(m):
        level = m.group(1)
        content = m.group(2).strip()
        content = re.sub(r"\\\*+", "", content)      # remove \* escape sequences
        content = re.sub(r"\*{2,}", " ", content)    # ** → space
        content = content.strip("* ").strip()
        return f"{level} {content}"
    return re.sub(r"^(#{1,6})\s+(.+)$", _clean, text, flags=re.MULTILINE)


def remove_orphaned_attributions(text: str) -> str:
    """Remove standalone short lines that are orphaned source citations.

    Targets lines like "Wikipedia", "Florida Museum", "gainesvillefl.gov"
    that appear as isolated attribution stubs from copy-paste.
    Heuristic: short (<= 40 chars), no markdown prefix, no sentence-ending
    punctuation, no digits, no colon, AND adjacent to at least one blank line.
    """
    lines = text.split("\n")
    result = []
    n = len(lines)

    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            result.append(line)
            continue
        if s[0] in "#*->|![":
            result.append(line)
            continue

        prev_blank = i == 0 or not lines[i - 1].strip()
        next_blank = i == n - 1 or not lines[i + 1].strip()
        is_isolated = prev_blank or next_blank

        if (
            is_isolated
            and len(s) <= 40
            and s[-1] not in ".!?,;:"
            and not re.search(r"\d", s)
            and ":" not in s
        ):
            continue  # drop orphaned attribution

        result.append(line)

    return "\n".join(result)


def normalize_whitespace(text: str) -> str:
    """Collapse 3+ consecutive blank lines to 2; strip trailing spaces per line."""
    lines = [ln.rstrip() for ln in text.split("\n")]
    result: list[str] = []
    blank_run = 0
    for line in lines:
        if not line:
            blank_run += 1
            if blank_run <= 2:
                result.append("")
        else:
            blank_run = 0
            result.append(line)
    return "\n".join(result).strip()


# ── Pipeline ──────────────────────────────────────────────────────────────────

def clean_document(text: str) -> str:
    text = decode_html_entities(text)
    text = remove_boilerplate_lines(text)
    text = strip_link_urls(text)
    text = remove_nav_text_lines(text)
    text = remove_cta_sections(text)
    text = remove_cta_paragraphs(text)
    text = remove_duplicate_title(text)
    text = fix_headers(text)
    text = remove_orphaned_attributions(text)
    text = normalize_whitespace(text)
    return text


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    md_files = sorted(INPUT_DIR.glob("*.md"))
    if not md_files:
        print(f"No markdown files found in {INPUT_DIR}/")
        return

    for path in md_files:
        raw = path.read_text(encoding="utf-8")
        cleaned = clean_document(raw)
        out_path = OUTPUT_DIR / path.name
        out_path.write_text(cleaned, encoding="utf-8")
        reduction = 100 * (1 - len(cleaned) / len(raw))
        print(f"  {path.name}: {len(raw):,} -> {len(cleaned):,} chars  ({reduction:.0f}% reduction)")

    print(f"\nDone. {len(md_files)} files written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
