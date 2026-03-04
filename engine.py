import os
import subprocess
import time
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

# ডিরেক্টরি সেটআপ
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ১. হোম পেজ (ল্যান্ডিং পেজ)
@app.route('/')
def index():
    return render_template('index.html')

# ২. প্রাইসিং পেজ
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# ৩. কন্টাক্ট পেজ
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ৪. মেইন এডিটিং ইঞ্জিন (Fast-Track)
@app.route('/edit', methods=['POST'])
def edit_video():
    if 'video' not in request.files:
        return "No file uploaded", 400
    
    video = request.files['video']
    text = request.form.get('text', 'AI MASTER PRO')
    
    input_p = os.path.join(UPLOAD_FOLDER, video.filename)
    output_p = os.path.join(OUTPUT_FOLDER, "processed_" + video.filename)
    video.save(input_p)

    # দ্রুত রেন্ডারিং কমান্ড (Ultrafast Preset)
    # এটি ভিডিওর গতি এবং কোয়ালিটি অপ্টিমাইজ করবে
    cmd = [
        'ffmpeg', '-y', '-i', input_p,
        '-vf', f"drawtext=text='{text}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '4', output_p
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return send_file(output_p, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
