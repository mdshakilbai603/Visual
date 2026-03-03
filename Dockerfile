# হাই-পারফরম্যান্স পাইথন ইমেজ
FROM python:3.10-slim

# ভিডিও এবং এআই লাইব্রেরি ইনস্টল (FFmpeg, OpenCV, ইত্যাদি)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# পাইথন লাইব্রেরিগুলো একবারে ইনস্টল করা
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# অ্যাপ্লিকেশন রান করা
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "engine:app"]
