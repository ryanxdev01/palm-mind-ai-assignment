
# Fixed-Size Chunking
def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """
    Divide text into fixed-size chunks with overlap.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be non-negative and smaller than chunk size."
        )

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# Recursive Character Chunking
def recursive_character_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """
    Split text using natural separators while respecting chunk size.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Overlap must be non-negative and smaller than chunk size."
        )

    text = text.strip()

    if not text:
        return []

    content_size = chunk_size - overlap
    separators = ["\n\n", "\n", ". ", " ", ""]

    def split_recursive(value: str, separator_index: int) -> list[str]:
        value = value.strip()

        if not value:
            return []

        if len(value) <= content_size:
            return [value]

        if separator_index >= len(separators):
            return [
                value[i:i + content_size]
                for i in range(0, len(value), content_size)
            ]

        separator = separators[separator_index]

        if separator == "":
            parts = list(value)
        else:
            parts = value.split(separator)

        result = []
        current = ""

        for part in parts:
            candidate = (
                current + separator + part if current else part
            )

            if len(candidate) <= content_size:
                current = candidate
            else:
                if current:
                    result.append(current)

                if len(part) > content_size:
                    result.extend(
                        split_recursive(part, separator_index + 1)
                    )
                    current = ""
                else:
                    current = part

        if current:
            result.append(current)

        return result

    raw_chunks = split_recursive(text, 0)

    final_chunks = []

    for index, chunk in enumerate(raw_chunks):
        if index == 0 or overlap == 0:
            final_chunks.append(chunk)
        else:
            previous = raw_chunks[index - 1]
            final_chunks.append(previous[-overlap:] + chunk)

    return final_chunks
