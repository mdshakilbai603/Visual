FROM python:3.10-slim

# FFmpeg এবং অন্যান্য সিস্টেম ফাইল
RUN apt-get update && apt-get install -y \
    ffmpeg git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ওপেন সোর্স লাইব্রেরি ইনস্টল
RUN pip install flask gunicorn openai-whisper gtts torch torchvision

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "engine:app", "--timeout", "0"]
