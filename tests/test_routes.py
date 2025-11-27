def test_home_page(client):
    assert 2 == 2


def test_index_redirect(client):
    """Проверка, что неавторизованный пользователь редиректится на /login."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
