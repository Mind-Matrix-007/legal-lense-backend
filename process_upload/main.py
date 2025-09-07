import os
import json
import requests
from google.cloud import storage, firestore

storage_client = storage.Client()
firestore_client = firestore.Client()

def process(event, context):
    bucket_name = event['bucket']
    file_name = event['name']

    # 1. Load file from GCS (simplified)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_content = blob.download_as_text()

    # 2. Fake text extraction (replace with your PDF extraction)
    text_json = {"text_preview": file_content[:1000]}

    # 3. Save extracted text to GCS
    results_bucket = os.environ.get("GCS_BUCKET")
    out_key = f"extracted/{file_name}.json"
    storage_client.bucket(results_bucket).blob(out_key).upload_from_string(
        json.dumps(text_json), content_type="application/json"
    )

    # 4. Save Firestore doc
    doc_id = file_name.replace(".pdf", "")
    firestore_client.collection("documents").document(doc_id).set({
        "text_blob": f"gs://{results_bucket}/{out_key}",
        "status": "TEXT_EXTRACTED"
    })

    # 5. ✅ Trigger Part C
    PROCESSOR_URL = os.environ.get("PROCESSOR_URL")
    if PROCESSOR_URL:
        try:
            requests.post(f"{PROCESSOR_URL}/process", json={"doc_id": doc_id}, timeout=10)
            print(f"Triggered processor_service for {doc_id}")
        except Exception as e:
            print(f"Error triggering processor_service: {e}")
