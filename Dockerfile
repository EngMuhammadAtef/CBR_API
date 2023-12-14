# Use an official TensorFlow image as the base image
FROM tensorflow/tensorflow:latest-gpu

# Install basic dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev ffmpeg libsm6 libxext6

# Install TensorRT dependencies
RUN apt-get install -y libnvinfer7 libnvinfer-dev libnvinfer-plugin7

# Set the LD_LIBRARY_PATH environment variable
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
