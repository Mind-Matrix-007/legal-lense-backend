# main.py
import os
import io
import fitz  # PyMuPDF for PDF text extraction (ensure it's in requirements.txt)
from flask import Flask, request, jsonify

from result_writer import ResultWriter

app = Flask(__name__)

# Initialize ResultWriter with bucket name from env var or fallback
BUCKET_NAME = os.getenv("PROCESSED_BUCKET", "legal-lense-processed")
writer = ResultWriter(bucket_name=BUCKET_NAME)


def extract_text_from_pdf(file_stream):
    """
    Extract text page by page from a PDF file.
    file_stream: bytes stream of the PDF
    Returns: list of page texts
    """
    doc = fitz.open(stream=file_stream, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text()
        pages.append(text)
    return pages


@app.route("/", methods=["POST"])
def process_file():
    """
    Expects JSON body:
    {
      "file_id": "abc123",
      "owner_id": "uid_456",
      "gcs_path": "gs://legal-lense-uploads/uploads/abc123.pdf"
    }
    """
    try:
        data = request.get_json()
        file_id = data.get("file_id")
        owner_id = data.get("owner_id")
        gcs_path = data.get("gcs_path")

        if not file_id or not owner_id or not gcs_path:
            return jsonify({"error": "file_id, owner_id, and gcs_path are required"}), 400

        # --- Step 1: Download file from GCS ---
        from google.cloud import storage
        storage_client = storage.Client()
        bucket_name, object_name = gcs_path.replace("gs://", "").split("/", 1)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        pdf_bytes = blob.download_as_bytes()

        # --- Step 2: Extract text from PDF ---
        pages = extract_text_from_pdf(io.BytesIO(pdf_bytes))
        extracted_text = "\n".join(pages)

        # --- Step 3: Dummy entities (in real pipeline you’d run NLP/regex/etc.) ---
        entities = {
            "clauses": ["Confidentiality", "Termination"],
            "dates": [],
            "parties": []
        }

        # --- Step 4: Write results to Firestore + GCS ---
        writer.save_result(
            file_id=file_id,
            owner_id=owner_id,
            extracted_text=extracted_text,
            pages=pages,
            entities=entities,
            processor_version="v1.0"
        )

        return jsonify({
            "status": "success",
            "message": f"Processed and saved results for {file_id}",
            "page_count": len(pages)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

