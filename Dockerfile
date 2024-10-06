FROM python:3.9.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["gunicorn", "--log-level", "debug", "-b", "0.0.0.0:5005", "app:app"]