FROM python:3.6-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN apt-get install ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "/usr/src/app/jackIntrBot.py" ]