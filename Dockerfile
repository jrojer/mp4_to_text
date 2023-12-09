FROM jrottenberg/ffmpeg:4.4-alpine

RUN apk add --no-cache \
    python3 \
    py3-pip

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir \
    openai \
    python-dotenv \
    tenacity

