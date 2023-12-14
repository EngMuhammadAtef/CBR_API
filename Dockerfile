FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr libtesseract-dev ffmpeg libsm6 libxext6 && \
    apt-get -qq -y install libnvinfer7 libnvinfer-dev libnvinfer-plugin7

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]