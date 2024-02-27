FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 9000
WORKDIR /app

RUN pip install poetry && \
    poetry config virtualenvs.in-project false

COPY pyproject.toml ./

RUN poetry install --no-dev

COPY . ./

CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]
