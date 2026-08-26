from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
}


def load_text_file(
    file_path: Path,
) -> str:

    try:

        return file_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError as exc:

        raise ValueError(
            f"Unable to decode file: "
            f"{file_path}"
        ) from exc