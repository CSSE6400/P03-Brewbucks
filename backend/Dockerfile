FROM python:3.11

RUN pip3 install poetry

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-root

COPY brewbucks brewbucks

EXPOSE 80 

CMD ["poetry", "run", "flask", "--app", "brewbucks", "run", "--host", "0.0.0.0", "--port", "80"]