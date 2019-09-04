from flask_api import status


def test_hello(client):
    response = client.get('/amalgamation/hello')

    assert response.status_code == status.HTTP_200_OK
