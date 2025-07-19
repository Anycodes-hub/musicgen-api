FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libavfilter-dev libswscale-dev libswresample-dev && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 10000

# Start app
CMD ["python", "app.py"]
