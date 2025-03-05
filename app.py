from flask import Flask, request, send_file
import subprocess
import uuid
import shutil
import os

app = Flask(__name__)

@app.route('/')
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return 'Missing URL parameter', 400
    
    temp_dir = f"/tmp/{uuid.uuid4().hex}"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        subprocess.run([
            'yt-dlp',
            '-f', 'worstvideo+worstaudio',
            '--merge-output-format', 'mp4',
            '-o', f'{temp_dir}/%(title)s.%(ext)s',
            video_url
        ], check=True, timeout=600)

        downloaded_file = os.listdir(temp_dir)[0]
        return send_file(
            os.path.join(temp_dir, downloaded_file),
            mimetype='video/mp4',
            as_attachment=False
        )
    except Exception as e:
        return f'Error: {str(e)}', 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3234)