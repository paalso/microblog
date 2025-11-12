# Microblog

based on

[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) / [Мега-Учебник Flask](https://habr.com/ru/articles/804245/)

by [Miguel Grinberg](https://blog.miguelgrinberg.com/author/Miguel%20Grinberg)

## 🚀 Local development setup

Clone the repository:

```bash
git clone https://github.com/paalso/microblog.git
cd microblog
```

Initialize the local environment:

```bash
make setup
```

This command will:

- create the instance/ directory (if missing),

- install dependencies via uv,

- apply all database migrations.

Then run the dev server:

```bash
make dev
```

Open your app at http://localhost:5001

### Useful links

[Flask's quick start page](https://flask.palletsprojects.com/en/stable/quickstart/)

[Gravatar](https://gravatar.com/)
