SELECT
  u.username, COUNT(*)
FROM users u
LEFT JOIN posts p
ON p.user_id = u.id
GROUP BY u.username
ORDER BY u.username;


SELECT * FROM followers;
--follower_id  followed_id
-------------  -----------
--1            2
--1            3
--2            1
--2            4
--3            1
--3            5
--4            1
--5            2


--followers per followed
SELECT
  u1.id, u1.username AS followed, f.follower_id AS follower_id, u2.username AS follower
FROM users u1
LEFT JOIN followers f ON u1.id = f.followed_id
JOIN users u2 ON u2.id = follower_id
ORDER BY u1.id;
--id  followed  follower_id  follower
----  --------  -----------  --------
--1   admin     2            paalso
--1   admin     3            bob
--1   admin     4            tom
--2   paalso    1            admin
--2   paalso    5            alice
--3   bob       1            admin
--4   tom       2            paalso
--5   alice     3            bob


--followed per followers
SELECT
  u1.id, u1.username AS follower, f.followed_id AS followed_id, u2.username AS followed
FROM users u1
LEFT JOIN followers f ON u1.id = f.follower_id
JOIN users u2 ON u2.id = followed_id
ORDER BY u1.id;
--id  follower  followed_id  followed
----  --------  -----------  --------
--1   admin     2            paalso
--1   admin     3            bob
--2   paalso    1            admin
--2   paalso    4            tom
--3   bob       1            admin
--3   bob       5            alice
--4   tom       1            admin
--5   alice     2            paalso



--=============================================================================
--following = relationship(     // (на кого я подписан)
--    secondary=followers,
--    primaryjoin=(followers.c.follower_id == id),
--    secondaryjoin=(followers.c.followed_id == id),
--    back_populates='followers'
--)

--following = список пользователей, на кого подписан текущий пользователь.

--Расшифровка:
--primaryjoin указывает условие, которое связывает объект с ассоциативной таблицей.
--primaryjoin: followers.follower_id == User.id
--→ найти строки, где этот User — подписчик
SELECT * FROM followers
WHERE follower_id = 2;
--follower_id  followed_id
-------------  -----------
--2            1
--2            4

--secondaryjoin указывает условие, которое связывает ассоциативную таблицу с пользователем на другой стороне связи.
-- ....
--secondaryjoin: followers.followed_id == User.id
--→ взять из этих строк тех, на кого он подписан
WITH my_followings AS (
    SELECT * FROM followers
    WHERE follower_id = 2
)
SELECT
    u.id, u.username
FROM users u
JOIN my_followings f ON u.id = f.followed_id;
--id  username
----  --------
--1   admin
--4   tom
--=============================================================================
--followers = relationship(         // (кто на меня подписан)
--    secondary=followers,
--    primaryjoin=(followers.c.followed_id == id),
--    secondaryjoin=(followers.c.follower_id == id),
--    back_populates='following'
--)
--followers = список пользователей, которые подписаны на текущего пользователя.

--Расшифровка:

-- primaryjoin=(followers.c.followed_id == id)
--→ выбираем строки таблицы followers, где
-- followed_id = текущий user.id
SELECT * FROM followers
WHERE followed_id = 2;
--follower_id  followed_id
-------------  -----------
--1            2
--5            2

-- ....
-- secondaryjoin=(followers.c.follower_id == id)
--→ затем соединяем с таблицей users по users.id = follower_id
WITH my_followed AS (
    SELECT * FROM followers
    WHERE followed_id = 2
)
SELECT
    u.id, u.username
FROM users u
JOIN my_followed f ON u.id = f.follower_id;
--id  username
----  --------
--1   admin
--5   alice