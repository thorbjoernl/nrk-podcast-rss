FROM python:3.11.4-alpine3.17

COPY . /app

WORKDIR "/app"
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "./app.py"]