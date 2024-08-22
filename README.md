# Biblioteca

An API for interacting with a database of books that are added and rated by users.

- A user needs to be created.
- To retrieve all books with their average rating, no user login is needed.
- To create, update, delete or rate a book, user login must be done first.
- A user can rate his or someone else's book only once. They can update their rating after.

## Instructions to run locally on Ubuntu
Make sure you have PostgreSQL installed: `sudo apt install postgresql`.

Run `conda env create -f environment.yml` to create a conda environment and install all dependencies with `poetry install`.

Fill in your local DB credentials in `.env` on the root directory of this repository like so:
```
    DATABASE_HOSTNAME=...
    DATABASE_PORT=...
    DATABASE_NAME=...
    DATABASE_USERNAME=...
    DATABASE_PASSWORD=...
    SECRET_KEY=...
    ALGORITHM=...
    ACCESS_TOKEN_EXPIRE_MINUTES=...
```

Then run `uvicorn app.main:app --host 0.0.0.0 --port 8000` to run the API locally and test it by making requests. See the Swagger documentation by navigating in your browser to `http://localhost:8000/docs`.
