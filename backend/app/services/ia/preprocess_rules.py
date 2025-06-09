def split_rules_into_chunks(file_path: str, max_chars: int = 512) -> list[str]:
    """
    Splits the MTG rules text into smaller chunks for embedding.

    Args:
        file_path (str): Path to the full rules text file.
        max_chars (int): Maximum number of characters per chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for section in sections:
        if len(current_chunk) + len(section) < max_chars:
            current_chunk += section + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = section + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
