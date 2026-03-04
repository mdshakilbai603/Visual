import os
import subprocess
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# ফোল্ডার সেটিংস
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit_video():
    if 'video' not in request.files:
        return "No file uploaded", 400
    
    video = request.files['video']
    text = request.form.get('text', 'AI MASTER PRO')
    
    input_p = os.path.join(UPLOAD_FOLDER, video.filename)
    output_p = os.path.join(OUTPUT_FOLDER, "processed_" + video.filename)
    video.save(input_p)

    # FFmpeg কমান্ড: ভিডিওতে টেক্সট বসানো এবং অপ্টিমাইজ করা
    cmd = [
        'ffmpeg', '-y', '-i', input_p,
        '-vf', f"drawtext=text='{text}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-movflags', 'faststart', output_p
    ]
    
    try:
        subprocess.run(cmd, check=True)
        # 'as_attachment=False' করা হয়েছে যাতে ভিডিওটি ব্রাউজারে প্লে হয়
        return send_file(output_p, mimetype='video/mp4', as_attachment=False)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Render এর জন্য ডিফল্ট পোর্ট
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
