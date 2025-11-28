
from app import db
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

    u1_following = set(u1.following)
    u2_followers = set(u2.followers)
    u1_following_usernames = set(u.username for u in u1_following)
    u2_followers_usernames = set(u.username for u in u2_followers)

    assert u1_following_usernames == {'susan', 'tom'}
    assert u2_followers_usernames == {'john'}

    # unfollow
    u1.unfollow(u2)
    db.session.commit()

    assert not u1.is_following(u2)
    assert u1.is_following(u3)
    assert u1.following_count() == 1
    assert u2.followers_count() == 0
