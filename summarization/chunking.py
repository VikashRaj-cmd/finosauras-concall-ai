CHARS_PER_CHUNK = 12000  # ~3000 tokens at ~4 chars/token


def chunk_transcript(text: str, chunk_size: int = CHARS_PER_CHUNK) -> list[str]:
    """
    Split transcript into chunks of ~chunk_size characters.
    Splits at paragraph boundaries (double newlines) to avoid cutting mid-sentence.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > chunk_size and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks
