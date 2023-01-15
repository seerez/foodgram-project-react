FROM python:3.7-slim

WORKDIR /app

COPY ./ .

RUN apt update && \
    apt upgrade -y && \
    apt -y install gcc && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]

