FROM python:3.10-slim

# ভিডিও প্রসেসিং এবং ক্লাউড টুলস ইনস্টল
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# সব লাইব্রেরি একসাথে ইনস্টল
RUN pip install --no-cache-dir \
    flask \
    gunicorn \
    stripe \
    opencv-python \
    moviepy \
    torch \
    google-cloud-storage

COPY . .

# অটোমেটিক ইঞ্জিন স্টার্ট
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "engine:app", "--timeout", "0"]
