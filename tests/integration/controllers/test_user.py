from http import HTTPStatus


def test_get_user_sucess(client):
    response = client.get("/users/")
    assert  response.status_code == HTTPStatus.OK