FROM python:3.10-slim

# শুধুমাত্র প্রয়োজনীয় FFmpeg ইনস্টল
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# timeout ১০০০ সেকেন্ড করা হলো যাতে সতর্কবার্তা না আসে
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "engine:app", "--timeout", "1000", "--workers", "1", "--threads", "2"]
