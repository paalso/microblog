>>> db.session.scalar(sa.select(User))
<User admin>

GET
>>> db.session.get(User, 2)
<User paalso>


FILTER BY
>>> db.session.query(User).filter_by(email='paalso@gmail.com').first()
<User paalso>
>>> db.session.query(User).filter_by(email='paalso@gmail.com')
<flask_sqlalchemy.query.Query object at 0x7f5641a89870>
>>> list(db.session.query(User).filter_by(email='paalso@gmail.com'))
[<User paalso>]


SELECT - получить всех Users
>>> users = db.session.scalars(sa.select(User)).all()
>>> users
[<User admin>, <User paalso>, <User bob>, <User tom>]


SELECT - получить только emails всех Users
>>> emails = db.session.scalars(sa.select(User.email)).all()
>>> emails
['admin@example.com', 'bob@email.net', 'paalso@gmail.com', 'tom@email.net']


SELECT — найти пользователя по email
>>> user = db.session.scalars(sa.select(User).where(User.email == "bob@email.net")).first()
>>> user
<User bob>


SELECT — фильтр + сортировка
>>> selected_users = db.session.scalars(
...         sa.select(User)
...         .where(User.username.like("%o%"))
...         .order_by(User.email.desc())
...     ).all()
>>> selected_users
[<User tom>, <User paalso>, <User bob>]


SELECT — несколько полей
rows = db.session.scalars(sa.select(User.id, User.username)).all()
>>> rows = db.session.execute(sa.select(User.id, User.username)).all()
>>> rows
[(1, 'admin'), (3, 'bob'), (2, 'paalso'), (4, 'tom')]


SELECT — получить одного и упасть если нет
>>> user = db.session.scalars(sa.select(User).where(User.id == 1)).one()
>>> user
<User admin>
>>> user = db.session.scalars(sa.select(User).where(User.id == 10)).one()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/paalso/Courses/microblog/.venv/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 1815, in one
    return self._only_one_row(
  File "/home/paalso/Courses/microblog/.venv/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 760, in _only_one_row
    raise exc.NoResultFound(
sqlalchemy.exc.NoResultFound: No row was found when one was required

SELECT — получить одного и None если нет
>>> user = db.session.scalars(sa.select(User).where(User.id == 10)).one_or_none()
>>> user
>>> user is None
True


SCALARS vs EXECUTE
execute() - возвращает строки SQL → кортежи значений.
scalars() - возвращает первую колонку из каждой строки → удобно для ORM.
>>> scalars = db.session.scalars(sa.select(User)).all()
>>> scalars
[<User admin>, <User paalso>, <User bob>, <User tom>]

>>> rows = db.session.execute(sa.select(User)).all()
>>> rows
[(<User admin>,), (<User paalso>,), (<User bob>,), (<User tom>,)]
