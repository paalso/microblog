--https://sqlime.org/

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    role VARCHAR(20) DEFAULT 'user',
    about_me VARCHAR(140)
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body VARCHAR(256) NOT NULL UNIQUE,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE followers (
    follower_id INTEGER NOT NULL REFERENCES users(id),
    followed_id INTEGER NOT NULL REFERENCES users(id),
    PRIMARY KEY (follower_id, followed_id)
);


INSERT INTO users (username, email) VALUES
    ('admin', 'admin@example.com'),
    ('paalso', 'paalso@gmail.com'),
    ('bob', 'bob@email.net'),
    ('tom', 'tom@email.net'),
    ('alice', 'alice@example.com');

UPDATE users
SET role = 'admin'
WHERE username = 'admin';

INSERT INTO posts (body, user_id) VALUES
    ('Hello everyone, this is my first post!', 1),
    ('Working on a new SQL project today.', 2),
    ('It’s a sunny day outside, perfect for coding.', 3),
    ('Trying out SQLite foreign keys — looks good!', 1),
    ('Just finished writing a Flask view, feeling great.', 4),
    ('Reading about window functions in SQL.', 2),
    ('Testing unique constraints on posts table.', 1),
    ('Coffee + coding = perfect morning.', 5),
    ('Preparing for an interview, practicing JOINs.', 5),
    ('This platform really helps me debug SQL queries.', 5);

INSERT INTO followers (follower_id, followed_id) VALUES
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 4),
    (3, 1),
    (3, 5),
    (4, 1),
    (5, 2);
