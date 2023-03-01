FROM python:3.9-slim

ARG BASE_PATH=/code
WORKDIR $BASE_PATH

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python3 ./people_also_ask/app.py"]