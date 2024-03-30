from flask import Flask, send_file, jsonify
from google.cloud import storage
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import datetime
import os
# Initialize Flask app
app = Flask(__name__)

# Google Cloud Storage setup
storage_client = storage.Client()
bucket_name = 'yourtranscript'
bucket = storage_client.get_bucket(bucket_name)

# Define route for retrieving transcript
@app.route('/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        # Fetching the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Formatting the transcript into text format
        formatter = JSONFormatter()
        json_transcript = formatter.format_transcript(transcript)

        # Create a blob in Google Cloud Storage
        blob = bucket.blob(f"{video_id}_transcript.json")

        # Uploading the transcript text as a blob
        blob.upload_from_string(json_transcript, content_type='application/json')

         # Generate a signed URL for the blob
        signed_url = blob.generate_signed_url(
            expiration=datetime.timedelta(minutes=15),  # Link expires in 15 minutes
            method='GET'
        )
        # Return the signed URL in the response
        return jsonify({'url': signed_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)