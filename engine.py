import os
import subprocess
from flask import Flask, render_template, request, send_file
from gtts import gTTS 
import whisper

app = Flask(__name__)

# ফোল্ডার তৈরি
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Whisper মডেল লোড (ওপেন সোর্স)
model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render_engine():
    if 'video' not in request.files:
        return "No video file uploaded", 400
        
    video = request.files['video']
    task = request.form.get('task')
    target_lang = request.form.get('target_lang', 'bn')
    
    input_p = os.path.join(UPLOAD_FOLDER, video.filename)
    output_p = os.path.join(OUTPUT_FOLDER, "AI_MASTER_" + video.filename)
    video.save(input_p)

    if task == "dubbing":
        # ১. অডিও বের করা
        audio_temp = "temp.mp3"
        subprocess.run(f"ffmpeg -i '{input_p}' -vn -acodec mp3 '{audio_temp}' -y", shell=True)
        
        # ২. ভয়েস টু টেক্সট (Whisper)
        result = model.transcribe(audio_temp)
        
        # ৩. ট্রান্সলেশন ও ভয়েস জেনারেশন (gTTS)
        tts = gTTS(text=result['text'], lang=target_lang)
        dubbed_audio = "dubbed.mp3"
        tts.save(dubbed_audio)

        # ৪. ভিডিওর সাথে নতুন ভয়েস মার্জ করা
        subprocess.run(f"ffmpeg -i '{input_p}' -i '{dubbed_audio}' -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_p}' -y", shell=True)
        
    elif task == "slowmo":
        subprocess.run(f"ffmpeg -i '{input_p}' -vf 'setpts=2*PTS' '{output_p}' -y", shell=True)
    
    elif task == "upscale":
        # ওপেন সোর্স স্কেলিং
        subprocess.run(f"ffmpeg -i '{input_p}' -vf scale=1280:-1 '{output_p}' -y", shell=True)

    return send_file(output_p, mimetype='video/mp4')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
