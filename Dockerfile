FROM python:3.11-slim

WORKDIR /app

COPY app.py .
COPY index.html .
COPY dashboard.html .

RUN pip install flask

ENV PORT 8080

CMD ["python", "app.py"]
