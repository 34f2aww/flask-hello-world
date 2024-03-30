from flask import Flask, send_file, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import os

app = Flask(__name__)

@app.route('/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        # Fetching the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Formatting the transcript into JSON
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript)

        # Writing the transcript to a file
        filename = f"{video_id}_transcript.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text_transcript)

        # Return the file
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)