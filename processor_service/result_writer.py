# result_writer.py
import json
from google.cloud import storage, firestore
from google.api_core.exceptions import GoogleAPICallError, RetryError

# read bucket name from env or hardcode during dev
DEFAULT_BUCKET = "legal-lense-processed"

class ResultWriter:
    def __init__(self, bucket_name=None):
        self.bucket_name = bucket_name or DEFAULT_BUCKET
        self.storage_client = storage.Client()
        self.db = firestore.Client()

    def _upload_string(self, gcs_path, content, content_type="text/plain"):
        """
        gcs_path: path like "fulltexts/{file_id}.txt"
        returns gs://... absolute path
        """
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(gcs_path)
        blob.upload_from_string(content, content_type=content_type)
        return f"gs://{self.bucket_name}/{gcs_path}"

    def save_result(self, file_id, owner_id, extracted_text, pages, entities, processor_version="v1"):
        """
        pages: list of page text strings (can be empty)
        entities: dict/list of extracted entities
        """
        try:
            # 1) Upload full text
            fulltext_path = f"fulltexts/{file_id}.txt"
            gcs_fulltext = self._upload_string(fulltext_path, extracted_text, "text/plain")

            # 2) Upload entities JSON
            entities_path = f"entities/{file_id}.json"
            gcs_entities = self._upload_string(entities_path, json.dumps(entities), "application/json")

            # 3) Upload pages (optional)
            for i, page_text in enumerate(pages, start=1):
                gcs_page_path = f"pages/{file_id}/page-{i}.txt"
                self._upload_string(gcs_page_path, page_text, "text/plain")

            # 4) Write results document
            result_ref = self.db.collection("results").document(file_id)
            result_ref.set({
                "fileId": file_id,
                "ownerId": owner_id,
                "summaryText": (extracted_text or "")[:1000],
                "gcsFullTextPath": gcs_fulltext,
                "entitiesPath": gcs_entities,
                "pageCount": len(pages),
                "entitiesCount": len(entities) if entities is not None else 0,
                "processorVersion": processor_version,
                "status": "completed",
                "processingTimestamp": firestore.SERVER_TIMESTAMP
            }, merge=True)

            # 5) Update uploads doc
            uploads_ref = self.db.collection("uploads").document(file_id)
            uploads_ref.update({
                "status": "completed",
                "processingCompletedAt": firestore.SERVER_TIMESTAMP,
                "resultId": file_id
            })

            return True
        except (GoogleAPICallError, RetryError, Exception) as e:
            # attempt to mark upload as failed and log error
            try:
                uploads_ref = self.db.collection("uploads").document(file_id)
                uploads_ref.update({
                    "status": "failed",
                    "errorMessage": str(e),
                    "processingCompletedAt": firestore.SERVER_TIMESTAMP
                })
            except Exception:
                pass
            raise
