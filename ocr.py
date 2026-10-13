from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
import re


PDF_FOLDER = "sample_pdfs"

print("OCR script started")
def normalize_text(text):

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


def ocr_pdf(pdf_path):

    try:

        pages = convert_from_path(pdf_path)

        results = []

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            text = pytesseract.image_to_string(
                page
            )

            normalized = normalize_text(
                text
            )

            quality = "OK"

            if len(normalized) < 20:

                quality = "LOW_QUALITY"

            results.append(
                {
                    "page": page_number,
                    "quality": quality,
                    "text": normalized
                }
            )

        return {
            "status": "success",
            "pages": results
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


def main():
    print("Running OCR...")


    scanned_files = [
        "INVOICE.pdf",
        "EMPLOYEE APPLICATION FORM.pdf"
    ]

    for filename in scanned_files:

        print(
            f"\nProcessing: {filename}"
        )

        result = ocr_pdf(
            Path(PDF_FOLDER) / filename
        )

        print(result)


if __name__ == "__main__":
    main()