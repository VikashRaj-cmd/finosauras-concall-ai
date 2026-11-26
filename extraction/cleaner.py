import re


def clean_transcript(text: str) -> str:
    """
    Clean raw PDF-extracted text for concall transcripts.
    Removes page numbers, repeated headers/footers, excess whitespace.
    """
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        # Skip blank lines (we'll re-add paragraph breaks)
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        # Skip standalone page numbers: "1", "Page 1", "- 1 -", "1 of 40"
        if re.fullmatch(r"[-–]?\s*\d+\s*[-–]?", line):
            continue
        if re.fullmatch(r"[Pp]age\s+\d+(\s+of\s+\d+)?", line):
            continue

        # Skip common repeated footer/header patterns
        if re.search(r"(confidential|all rights reserved|www\.|©|\bpdf\b)", line, re.I):
            if len(line) < 80:  # short lines only — long lines may be content
                continue

        cleaned.append(line)

    text = "\n".join(cleaned)

    # Collapse 3+ consecutive newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix broken words across lines (word- \n word → word word)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Normalize multiple spaces
    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def detect_quarter(text: str) -> str:
    """
    Try to detect the quarter from transcript text.
    Returns e.g. "Q2 FY26" or empty string.
    """
    # Match patterns like "Q2 FY2026", "Q2FY26", "second quarter FY26"
    match = re.search(
        r"Q([1-4])\s*FY\s*(\d{2,4})",
        text[:3000],  # check only first 3000 chars
        re.IGNORECASE,
    )
    if match:
        q = match.group(1)
        fy = match.group(2)
        if len(fy) == 4:
            fy = fy[2:]  # 2026 → 26
        return f"Q{q} FY{fy}"

    # Match "first/second/third/fourth quarter"
    word_map = {"first": "1", "second": "2", "third": "3", "fourth": "4"}
    match = re.search(
        r"(first|second|third|fourth)\s+quarter.*?FY\s*(\d{2,4})",
        text[:3000],
        re.IGNORECASE,
    )
    if match:
        q = word_map.get(match.group(1).lower(), "?")
        fy = match.group(2)
        if len(fy) == 4:
            fy = fy[2:]
        return f"Q{q} FY{fy}"

    return ""
