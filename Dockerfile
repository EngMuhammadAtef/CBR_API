# Use the official TensorFlow image as the base image
FROM tensorflow/tensorflow:latest

# Update the package list and install additional dependencies
RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr && \
    apt-get -qq -y install libtesseract-dev && \
    apt-get -qq -y install ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]