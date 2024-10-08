FROM python:3.11.6

RUN pip install poetry==1.8.3

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-cache 

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry", "run"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
