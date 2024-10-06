from flask import Flask, send_file, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
#from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.formatters import TextFormatter

from os import getenv

# for videos without subtitles #
#import whisper
#from langdetect import detect
#from pytube import YouTube
# for videos without subtitles #
app = Flask(__name__)

@app.route('/<video_id>', methods=['GET'])
def get_transcript(video_id):
    username=getenv('USERNAME')
    password=getenv('PASSWORD')

    MAX_RETRIES = 10  # Define the maximum number of attempts
    success = False   # Track success

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Fetching the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": f"http://{username}:{password}@p.webshare.io:80"},languages=['en', 'zh', 'zh-CN'])

            # Formatting the transcript into JSON
            #formatter = JSONFormatter()
            #json_transcript = formatter.format_transcript(transcript)

            # Formatting the transcript into TEXT
            success = True
            formatter = TextFormatter()
            txt_transcript = formatter.format_transcript(transcript)

            # Writing the transcript to a file
            filename = f"/tmp/" +f"{video_id}_transcript.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(txt_transcript)

            # Return the file
            return send_file(filename, as_attachment=True)
        except Exception as e: 
            print(f"Attempt {attempt} failed with error: {e}")

    if not success:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)



# from pytube import YouTube
# yt = YouTube('video_URL')
# audio = yt.streams.filter(only_audio=True).first()
# audio.download()