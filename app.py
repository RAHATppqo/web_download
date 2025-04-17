from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format', 'mp4')

    if not url:
        return "URL is required", 400

    download_id = str(uuid.uuid4())
    folder = 'downloads'
    os.makedirs(folder, exist_ok=True)

    outtmpl = os.path.join(folder, f"{download_id}.%(ext)s")

    ydl_opts = {
        'outtmpl': outtmpl,
        'quiet': True,
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format_type == 'mp3' else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == 'mp3':
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Download error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
