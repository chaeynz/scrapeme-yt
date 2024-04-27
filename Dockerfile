FROM python:3.10-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "launch:app"]
