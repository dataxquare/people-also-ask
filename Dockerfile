FROM python:3.9-slim

ARG BASE_PATH=/code
WORKDIR $BASE_PATH

COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry lock --no-update
RUN poetry install --no-dev

EXPOSE 8080
CMD ["poetry", "run", "start"]