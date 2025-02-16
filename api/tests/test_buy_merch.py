import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create_user(username="buyer", password="pass")
    return user


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


def test_buy_merch(auth_client, mocker):
    mock_response = {"message": "Purchase successful"}
    mocker.patch("requests.get",
                 return_value=mocker.Mock(json=lambda: mock_response,
                                          status_code=200))

    response = auth_client.get("/api/buy/t-shirt/")
    assert response.status_code == 200
    assert response.json() == mock_response
