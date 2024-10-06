from flask import Flask, send_file, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
#from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.formatters import TextFormatter

import os

# for videos without subtitles #
#import whisper
#from langdetect import detect
#from pytube import YouTube
# for videos without subtitles #
app = Flask(__name__)

@app.route('/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        # Fetching the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh', 'zh-CN'])

        # Formatting the transcript into JSON
        #formatter = JSONFormatter()
        #json_transcript = formatter.format_transcript(transcript)
        formatter = TextFormatter()
        json_transcript = formatter.format_transcript(transcript)

        # Writing the transcript to a file
        filename = f"/tmp/" +f"{video_id}_transcript.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json_transcript)

        # Return the file
        return send_file(filename, as_attachment=True)

    except Exception as e: # if video has no subtitles
        # try:
        #     url = f"https://www.youtube.com/watch?v={video_id}"
        #     yt = YouTube(url)
        #     # Get the audio stream
        #     audio_stream = yt.streams.filter(only_audio=True).first()
        #     # Download the audio stream
        #     audio_stream.download(output_paht="/tmp", filename=f"{video_id}.mp3")

        #     # Load the model
        #     model = whisper.load_model("base")
        #     result = model.transcribe(f"/tmp/{video_id}.mp3")
        #     transcribed_text = result["text"]

        #     # Create and open a txt file with the text
        #     filename = f"/tmp/" +f"{video_id}_whisper_tran.txt"
        #     with open(filename, "w", encoding="utf-8") as file:
        #         file.write(transcribed_text)

        #     # Return the file
        #     return send_file(filename, as_attachment=True)

        # except Exception as n:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
