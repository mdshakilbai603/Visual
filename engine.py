import os
import subprocess
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit_engine():
    video = request.files['video']
    task = request.form.get('task')
    
    in_path = os.path.join(UPLOAD_FOLDER, video.filename)
    out_path = os.path.join(OUTPUT_FOLDER, "FINAL_EDIT_" + video.filename)
    video.save(in_path)

    # এডিটিং প্রসেস (FFmpeg ফিল্টার যা CapCut-এর মতো কাজ করে)
    if task == "cinematic":
        # হাই কন্ট্রাস্ট এবং কালার বুস্ট
        cmd = f"ffmpeg -i '{in_path}' -vf \"eq=brightness=0.03:contrast=1.3:saturation=1.5,unsharp=5:5:1.0:5:5:0.0\" -c:a copy '{out_path}' -y"
    
    elif task == "slowmo":
        # স্মুথ স্লো মোশন এবং অডিও অ্যাডজাস্ট
        cmd = f"ffmpeg -i '{in_path}' -vf \"setpts=2.5*PTS\" -af \"atempo=0.5\" '{out_path}' -y"
    
    elif task == "hdr":
        # এইচডিআর লুক (Sharpness + Dynamic Range)
        cmd = f"ffmpeg -i '{in_path}' -vf \"format=yuv420p,curves=all='0/0 0.5/0.46 1/1'\" -c:a copy '{out_path}' -y"
    
    elif task == "dubbing":
        # ফ্রি ডাবিং ভয়েস (মেমোরি ক্রাশ এড়াতে)
        from gtts import gTTS
        tts = gTTS(text="ভিডিওটি এআই মাস্টারের মাধ্যমে প্রসেস করা হয়েছে।", lang='bn')
        tts.save("voice.mp3")
        cmd = f"ffmpeg -i '{in_path}' -i voice.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{out_path}' -y"
    
    else:
        cmd = f"ffmpeg -i '{in_path}' -c copy '{out_path}' -y"

    subprocess.run(cmd, shell=True, check=True)
    return send_file(out_path, mimetype='video/mp4')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
