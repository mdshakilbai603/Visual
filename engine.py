import os
import subprocess
from flask import Flask, render_template, request, send_file
from gtts import gTTS

app = Flask(__name__)

# ডিরেক্টরি সেটআপ
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
for f in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(f, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render_engine():
    video = request.files['video']
    task = request.form.get('task')
    target_lang = request.form.get('target_lang', 'bn')
    
    input_p = os.path.join(UPLOAD_FOLDER, video.filename)
    output_p = os.path.join(OUTPUT_FOLDER, "FINAL_" + video.filename)
    video.save(input_p)

    try:
        if task == "dubbing":
            # ডাবিং লজিক
            audio_temp = "temp.mp3"
            subprocess.run(f"ffmpeg -i '{input_p}' -vn -acodec mp3 '{audio_temp}' -y", shell=True, check=True)
            tts = gTTS(text="আপনার ভিডিওটি ডাবিং করা হয়েছে।", lang=target_lang)
            tts.save("voice.mp3")
            subprocess.run(f"ffmpeg -i '{input_p}' -i voice.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_p}' -y", shell=True, check=True)
            
        elif task == "color_grade":
            # সিনেমেটিক কালার ফিল্টার
            subprocess.run(f"ffmpeg -i '{input_p}' -vf \"eq=brightness=0.06:contrast=1.3:saturation=1.6\" -c:a copy '{output_p}' -y", shell=True, check=True)

        elif task == "slowmo":
            # স্লো মোশন
            subprocess.run(f"ffmpeg -i '{input_p}' -vf \"setpts=2.0*PTS\" -af \"atempo=0.5\" '{output_p}' -y", shell=True, check=True)

        elif task == "upscale":
            # এইচডি আপস্কেল
            subprocess.run(f"ffmpeg -i '{input_p}' -vf scale=1280:-1 '{output_p}' -y", shell=True, check=True)

        return send_file(output_p, mimetype='video/mp4')

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # এটি ৫০২ এরর সমাধান করবে
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
