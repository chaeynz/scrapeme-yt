FROM python:3.11-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt
RUN chmod +x patch_pytube.sh
RUN ./patch_pytube.sh

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "launch:app"]

ENV key=value