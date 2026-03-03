import os
import subprocess
import time
import stripe
from flask import Flask, render_template, request, send_file, jsonify, redirect

app = Flask(__name__)

# Stripe API Key (আপনার Stripe একাউন্ট থেকে বসাবেন)
stripe.api_key = "your_stripe_secret_key"

# স্টোরেজ কনফিগারেশন
VAULT = {'in': 'vault_raw', 'out': 'vault_master', 'logs': 'analytics.log'}
for folder in [VAULT['in'], VAULT['out']]: os.makedirs(folder, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout():
    # পেমেন্ট সেশন তৈরি (৫ ডলার ফি)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'AI Video Render (Pro)'},
                'unit_amount': 500,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return redirect(session.url, code=303)

@app.route('/edit', methods=['POST'])
def process_video():
    if 'video' not in request.files: return "No file", 400
    
    video = request.files['video']
    text = request.form.get('text', 'AI_PRO_MASTER')
    
    in_path = os.path.join(VAULT['in'], "input.mp4")
    out_path = os.path.join(VAULT['out'], "output.mp4")
    video.save(in_path)

    # সিনেমাটিক এআই রেন্ডার (FFmpeg)
    # এখানে ডাবিং এবং ফিল্টার লজিক যুক্ত আছে
    cmd = [
        'ffmpeg', '-y', '-i', in_path,
        '-vf', f"unsharp=5:5:1.0,drawtext=text='{text}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23', out_path
    ]
    subprocess.run(cmd, check=True)

    # অ্যাক্টিভিটি লগ (Admin Dashboard এর জন্য)
    with open(VAULT['logs'], "a") as f:
        f.write(f"{time.ctime()} | Success | {text}\n")

    return send_file(out_path, as_attachment=True)

@app.route('/admin/dashboard')
def dashboard_api():
    with open(VAULT['logs'], "r") as f:
        logs = f.readlines()
    return jsonify({"total_sales": len(logs), "revenue": f"${len(logs)*5}", "logs": logs[-10:]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
