from pathlib import Path
import re

from app.ingestion.schemas import DocumentMetadata


def extract_field(
    text: str,
    field_name: str,
) -> str | None:

    pattern = rf"^{re.escape(field_name)}:\s*(.+)$"

    match = re.search(
        pattern,
        text,
        re.MULTILINE,
    )

    if not match:
        return None

    return match.group(1).strip()


def extract_metadata(
    file_path: Path,
    knowledge_base_root: Path,
    text: str,
) -> DocumentMetadata:

    relative_path = file_path.relative_to(
        knowledge_base_root
    )

    parts = relative_path.parts

    if len(parts) < 4:
        raise ValueError(
            f"Unexpected knowledge-base path: "
            f"{relative_path}"
        )

    client = parts[0]

    district = parts[1]

    category = parts[2]

    document_name = parts[3]


    return DocumentMetadata(
        client=client,

        district=district,

        category=category,

        document_name=document_name,

        document_path=str(relative_path),

        version=extract_field(
            text,
            "Version",
        ),

        document_date=(
            extract_field(
                text,
                "Publication Date",
            )
            or
            extract_field(
                text,
                "Inspection Date",
            )
            or
            extract_field(
                text,
                "Effective Date",
            )
        ),

        asset_id=extract_field(
            text,
            "Asset ID",
        ),

        project_id=(
            extract_field(
                text,
                "Project Reference",
            )
            or
            extract_field(
                text,
                "Associated project",
            )
        ),

        inspection_id=extract_field(
            text,
            "Inspection ID",
        ),

        standard_reference=extract_field(
            text,
            "Standard Reference",
        ),
    )