FROM python:3.11.4-alpine3.17
COPY "poetry.lock" "/app/poetry.lock"
COPY "pyproject.toml" "/app/pyproject.toml"
WORKDIR "/app"
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY "." "."

CMD ["python", "./app.py"]