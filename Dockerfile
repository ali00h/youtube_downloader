FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir yt-dlp flask

COPY app.py /app/
WORKDIR /app

CMD ["python", "app.py"]