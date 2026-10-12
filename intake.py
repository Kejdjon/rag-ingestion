from pathlib import Path
from pypdf import PdfReader
import csv


PDF_FOLDER = "sample_pdfs"
OUTPUT_FILE = "classification_results.csv"


def classify_pdf(pdf_path):

    try:

        reader = PdfReader(pdf_path)

        page_count = len(reader.pages)

        extracted_text = ""

        for page in reader.pages[:3]:

            try:
                extracted_text += page.extract_text() or ""
            except Exception:
                pass

        if page_count == 0:

            return {
                "file": pdf_path.name,
                "status": "Rejected",
                "reason": "Empty PDF",
                "pages": 0,
                "classification": "N/A"
            }

        clean_text = extracted_text.strip()

        if len(clean_text) == 0:

            classification = "Scanned"
            processing = "OCR Required"

        elif len(clean_text) > 50:

            classification = "Text-Based"
            processing = "Direct Text Extraction"

        else:

            classification = "Scanned"
            processing = "OCR Required"

        return {
            "file": pdf_path.name,
            "status": "Accepted",
            "pages": page_count,
            "classification": classification,
            "processing": processing
        }

    except Exception:

        return {
            "file": pdf_path.name,
            "status": "Rejected",
            "pages": 0,
            "classification": "Invalid File",
            "processing": "None"
        }


def main():

    pdfs = Path(PDF_FOLDER).glob("*.pdf")

    results = []

    for pdf in pdfs:

        result = classify_pdf(pdf)

        print(result)

        results.append(result)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file",
                "status",
                "pages",
                "classification",
                "processing",
                "reason"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(
        f"\nClassification saved to "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()