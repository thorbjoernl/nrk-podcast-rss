FROM python:3.12.2-alpine3.19
COPY "poetry.lock" "/app/poetry.lock"
COPY "pyproject.toml" "/app/pyproject.toml"
WORKDIR "/app"
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY "." "."

CMD ["python", "./app.py"]