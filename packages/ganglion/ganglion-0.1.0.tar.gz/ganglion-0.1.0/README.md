# ganglion

The server that serves Textual apps in the browser.

Currently an early WIP

## Getting Started

Ganglion doesn't use any particular packaging ATM. Here's how to install:

- Create and activate a Python 3.11 venv:
- `pip install -r requirements.txt`
- `pip install -e .`

This will install a `ganglion` command on the path.

Install the front-end dependencies using `npm i`.
If you don't have `npm`, consider using [`nvm`](https://github.com/nvm-sh/nvm) (or [`nvm.fish`](https://github.com/jorgebucaran/nvm.fish)) to install it.
You can install the latest node and npm using `nvm install latest`.

To test, open *2* terminals, and activate the venvs.

On terminal A, run `DEBUG=1 ganglion serve`.
On terminal B, run `DEBUG=1 ganglion client`.

If all goes well you should be able to type in terminal B, and see the packets arrive on terminal A.

## Setting up a database for local development

### MacOS

- Install [Postgres.app](https://postgresapp.com/).
- Add `/Applications/Postgres.app/Contents/Versions/latest/bin` to your `PATH`.
- Run `psql` in your terminal, then run `CREATE DATABASE ganglion;` to create the required database.
- Leave `psql` (ctrl+d), and run `alembic upgrade head` to set up the initial database.
- Re-enter `psql` and run `\c ganglion` to connect to the `ganglion` database.
- Run `\dt` to list all the tables in the current database - you should see that tables have been created.

## Migrations

Create migration file:

```
alembic revision --autogenerate -m "Added account table"
```

Apply migration:

```
alembic upgrade head
```

See [Alembic](https://alembic.sqlalchemy.org/en/latest/) docs for details
