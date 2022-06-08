FROM python:3.9.13

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY src/ .

CMD ["python3", "./server.py"]
