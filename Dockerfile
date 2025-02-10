
FROM python:3.12

WORKDIR /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["gunicorn", "servlliance.wsgi", "--bind", "0.0.0.0:8080"]
