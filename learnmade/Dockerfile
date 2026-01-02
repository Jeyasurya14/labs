FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN useradd -m appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "learnmade.wsgi:application"]
