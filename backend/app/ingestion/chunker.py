import re


DEFAULT_MAX_CHARS = 1200


def split_markdown_sections(
    text: str,
) -> list[tuple[str | None, str]]:

    lines = text.splitlines()

    sections = []

    current_heading = None
    current_lines = []


    def save_current_section():

        if not current_lines:
            return

        content = "\n".join(
            current_lines
        ).strip()

        if not content:
            return

        sections.append(
            (
                current_heading,
                content,
            )
        )


    for line in lines:

        heading_match = re.match(
            r"^#{1,6}\s+(.+?)\s*$",
            line,
        )


        if heading_match:

            save_current_section()

            current_heading = (
                heading_match.group(1).strip()
            )

            current_lines = [
                line
            ]

        else:

            current_lines.append(line)


    save_current_section()

    return sections


def split_large_text(
    text: str,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[str]:

    text = text.strip()


    if not text:
        return []


    if len(text) <= max_chars:
        return [text]


    paragraphs = re.split(
        r"\n\s*\n",
        text,
    )


    chunks = []

    current = ""


    for paragraph in paragraphs:

        paragraph = paragraph.strip()


        if not paragraph:
            continue


        if not current:

            current = paragraph

            continue


        candidate = (
            current
            + "\n\n"
            + paragraph
        )


        if len(candidate) <= max_chars:

            current = candidate

        else:

            chunks.append(
                current
            )

            current = paragraph


    if current:

        chunks.append(
            current
        )


    final_chunks = []


    for chunk in chunks:

        if len(chunk) <= max_chars:

            final_chunks.append(
                chunk
            )

            continue


        start = 0


        while start < len(chunk):

            end = start + max_chars

            final_chunks.append(
                chunk[start:end].strip()
            )

            start = end


    return [
        chunk
        for chunk in final_chunks
        if chunk
    ]