from pathlib import Path

from app.ingestion.document_loader import (
    SUPPORTED_EXTENSIONS,
    load_text_file,
)

from app.ingestion.metadata_extractor import (
    extract_metadata,
)

from app.ingestion.schemas import (
    IngestedDocument,
)


class DocumentProcessor:

    def __init__(
        self,
        knowledge_base_root: Path,
    ):

        self.knowledge_base_root = (
            knowledge_base_root.resolve()
        )


    def discover_files(self) -> list[Path]:

        if not self.knowledge_base_root.exists():

            raise FileNotFoundError(
                "Knowledge base directory does "
                f"not exist: "
                f"{self.knowledge_base_root}"
            )


        files = []


        for path in self.knowledge_base_root.rglob("*"):

            if not path.is_file():
                continue


            if path.suffix.lower() not in (
                SUPPORTED_EXTENSIONS
            ):
                continue


            files.append(path)


        return sorted(files)


    def process_file(
        self,
        file_path: Path,
    ) -> IngestedDocument:

        text = load_text_file(
            file_path
        )


        metadata = extract_metadata(
            file_path=file_path,
            knowledge_base_root=(
                self.knowledge_base_root
            ),
            text=text,
        )


        return IngestedDocument(
            text=text,
            metadata=metadata,
        )


    def process_all(
        self,
    ) -> list[IngestedDocument]:

        files = self.discover_files()


        documents = []


        for file_path in files:

            document = self.process_file(
                file_path
            )

            documents.append(document)


        return documents