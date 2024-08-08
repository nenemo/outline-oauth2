FROM python:3.9-slim

WORKDIR /outline-gauth

COPY . .

RUN apt-get update && apt install -y git && pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
