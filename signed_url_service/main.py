import os
import datetime
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

# Env vars
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCS_BUCKET = os.environ.get("GCS_BUCKET")

storage_client = storage.Client(project=GCP_PROJECT)

@app.route("/get-signed-url", methods=["POST"])
def get_signed_url():
    try:
        data = request.get_json() or {}
        filename = data.get("filename")
        if not filename:
            return jsonify({"error": "filename required"}), 400

        if not GCS_BUCKET:
            return jsonify({"error": "GCS_BUCKET env var missing"}), 500

        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob(f"uploads/{filename}")

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=30),
            method="PUT",
            content_type="application/octet-stream",
        )

        return jsonify({
            "url": url,
            "gcs_path": f"gs://{GCS_BUCKET}/uploads/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
