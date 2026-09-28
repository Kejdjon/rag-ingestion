import json
import argparse
from pathlib import Path

from pypdf import PdfReader


def extract_text(file_path):
    pages = []

    if file_path.suffix.lower() == ".txt":
        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
        pages.append((1, text))

    elif file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))

        for page_num, page in enumerate(
            reader.pages,
            start=1
        ):
            pages.append(
                (page_num, page.extract_text() or "")
            )

    return pages


def clean_text(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return " ".join(lines)


def chunk_text(
        text,
        chunk_size=500,
        overlap=50):

    chunks = []
    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text)
        )

        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def ingest_documents(
        folder,
        chunk_size,
        overlap):

    all_chunks = []

    for file in Path(folder).glob("*"):

        if file.suffix.lower() not in [
            ".txt",
            ".pdf"
         ]:
            continue

        pages = extract_text(file)

        for page_num, text in pages:

            text = clean_text(text)

            chunks = chunk_text(
                text,
                chunk_size,
                overlap
            )

            for idx, chunk in enumerate(chunks):

                all_chunks.append({
                    "chunk": chunk,
                    "metadata": {
                        "source": file.name,
                        "page": page_num,
                        "chunk_id": idx
                    }
                })

    return all_chunks


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--docs",
        default="documents"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500
    )

    parser.add_argument(
        "--overlap",
        type=int,
        default=50
    )

    args = parser.parse_args()

    results = ingest_documents(
        args.docs,
        args.chunk_size,
        args.overlap
    )

    with open(
            "chunks.json",
            "w",
            encoding="utf-8") as f:

        json.dump(
            results,
            f,
            indent=2
        )

    print(
        f"Created {len(results)} chunks"
    )