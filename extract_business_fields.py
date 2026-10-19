import json
import re
from pathlib import Path

from invoice_schema import Invoice


INPUT_FOLDER = "di_output"
OUTPUT_FOLDER = "business_output"

Path(OUTPUT_FOLDER).mkdir(
    exist_ok=True
)


def extract_invoice_fields(doc):

    source = doc.get("source")

    if not doc.get("pages"):
        return Invoice(
            source_document=source
        )

    page = doc["pages"][0]

    text = page.get(
        "text",
        ""
    )

    page_number = page.get(
        "page_number",
        1
    )

    def find(pattern):
        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(1).strip()

        return None

    return Invoice(
        invoice_number=find(
            r"Invoice Number:\s*(INV-\d+)"
        ),
        customer=find(
            r"Customer:\s*(.*?)\sDate:"
        ),
        invoice_date=find(
            r"Date:\s*(.*?)\sServices Provided:"
        ),
        services_provided=find(
            r"Services Provided:\s*(.*?)\sAmount Due:"
        ),
        amount_due=find(
            r"Amount Due:\s*(.*?)\sThank"
        ),
        source_document=source,
        page_number=page_number
    )


def process_document(json_file):

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as f:

        doc = json.load(f)

    try:

        invoice = extract_invoice_fields(
            doc
        )

        return invoice

    except Exception:

        return Invoice(
            source_document=doc.get(
                "source"
            ),
            page_number=1
        )


def main():

    for file in Path(
        INPUT_FOLDER
    ).glob("*.json"):

        result = process_document(
            file
        )

        output_file = (
            Path(OUTPUT_FOLDER)
            / file.name
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result.model_dump(),
                f,
                indent=2
            )

        print(
            f"Processed {file.name}"
        )


if __name__ == "__main__":
    main()