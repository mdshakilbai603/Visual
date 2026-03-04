FROM python:3.10-slim

# FFmpeg এবং প্রয়োজনীয় সিস্টেম ফাইল ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# লাইব্রেরি ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render এর পোর্টের জন্য কনফিগারেশন
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "engine:app", "--timeout", "600"]
