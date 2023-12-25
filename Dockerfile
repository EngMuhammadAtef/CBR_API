FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr && \
    apt-get -qq -y install libtesseract-dev && \
    apt-get -qq -y install ffmpeg libsm6 libxext6 && \
    apt-get -qq -y install libatlas-base-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install TensorFlow
RUN pip3 install tensorflow

COPY . .

CMD ["gunicorn", "app:app"]
