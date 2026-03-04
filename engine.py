import os
import subprocess
from flask import Flask, render_template, request, send_file
from gtts import gTTS

app = Flask(__name__)

# ডিরেক্টরি সেটআপ
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
for d in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(d, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    video = request.files['video']
    task = request.form.get('task')
    
    in_path = os.path.join(UPLOAD_FOLDER, video.filename)
    out_path = os.path.join(OUTPUT_FOLDER, "FINAL_" + video.filename)
    video.save(in_path)

    # এডিটিং লজিক (FFmpeg)
    if task == "cinematic":
        cmd = f"ffmpeg -i '{in_path}' -vf \"eq=contrast=1.3:saturation=1.5:brightness=0.03\" -c:a copy '{out_path}' -y"
    elif task == "slowmo":
        cmd = f"ffmpeg -i '{in_path}' -vf \"setpts=2*PTS\" -af \"atempo=0.5\" '{out_path}' -y"
    elif task == "bw":
        cmd = f"ffmpeg -i '{in_path}' -vf \"hue=s=0\" -c:a copy '{out_path}' -y"
    elif task == "hdr":
        cmd = f"ffmpeg -i '{in_path}' -vf \"unsharp=5:5:1.0:5:5:0.0,eq=contrast=1.1\" -c:a copy '{out_path}' -y"
    elif task == "dubbing":
        # মেমোরি ক্রাশ এড়াতে সিম্পল ডাবিং
        tts = gTTS(text="আপনার এআই ভিডিও এডিটিং সফল হয়েছে।", lang='bn')
        tts.save("voice.mp3")
        cmd = f"ffmpeg -i '{in_path}' -i voice.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{out_path}' -y"
    else:
        cmd = f"ffmpeg -i '{in_path}' -c copy '{out_path}' -y"

    subprocess.run(cmd, shell=True, check=True)
    return send_file(out_path, mimetype='video/mp4')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
