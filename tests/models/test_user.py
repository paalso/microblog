from datetime import datetime, timedelta, timezone

from app import db
from app.models.post import Post
from app.models.user import User


def test_password_hashing():
    u = User(username='susan', email='susan@example.com')
    u.set_password('cat')
    assert not u.check_password('dog')
    assert u.check_password('cat')


def test_avatar():
    u = User(username='john', email='john@example.com')
    assert u.avatar(128) == ('https://www.gravatar.com/avatar/'
                                     'd4c74594d841139328695756648b6bd6'
                                     '?d=identicon&s=128')


def test_follow(app):
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='susan', email='susan@example.com')
    u3 = User(username='tom', email='tom@example.com')
    db.session.add_all([u1, u2])
    db.session.commit()

    # before following
    assert list(u1.following) == []
    assert list(u2.followers) == []
    assert list(u3.followers) == []

    # follow
    u1.follow(u2)
    u1.follow(u3)
    db.session.commit()

    assert u1.is_following(u2)
    assert u1.is_following(u3)
    assert u1.following_count() == 2
    assert u2.followers_count() == 1
    assert u3.followers_count() == 1

    u1_following = list(u1.following)
    u2_followers = list(u2.followers)

    assert u1_following[0].username == 'susan'
    assert u1_following[1].username == 'tom'
    assert u2_followers[0].username == 'john'

    # unfollow
    u1.unfollow(u2)
    db.session.commit()

    assert not u1.is_following(u2)
    assert u1.is_following(u3)
    assert u1.following_count() == 1
    assert u2.followers_count() == 0


def test_follow_posts(app):
    # create users
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='susan', email='susan@example.com')
    u3 = User(username='mary', email='mary@example.com')
    u4 = User(username='david', email='david@example.com')
    db.session.add_all([u1, u2, u3, u4])

    # create posts
    now = datetime.now(timezone.utc)
    p1 = Post(body="post from john", author=u1,
              created_at=now + timedelta(seconds=1))
    p2 = Post(body="post from susan", author=u2,
              created_at=now + timedelta(seconds=4))
    p3 = Post(body="post from mary", author=u3,
              created_at=now + timedelta(seconds=3))
    p4 = Post(body="post from david", author=u4,
              created_at=now + timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    # follow relations
    u1.follow(u2)
    u1.follow(u4)
    u2.follow(u3)
    u3.follow(u4)
    db.session.commit()

    # now get following posts
    f1 = u1.following_posts()
    f2 = u2.following_posts()
    f3 = u3.following_posts()
    f4 = u4.following_posts()

    # verify results
    import pdb; pdb.set_trace()
    assert f1 == [p2, p4, p1]
    # assert f2 == [p2, p3]
    # assert f3 == [p3, p4]
    # assert f4 == [p4]
