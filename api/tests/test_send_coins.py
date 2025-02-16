import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="sender", password="pass")


@pytest.fixture
def receiver():
    return User.objects.create_user(username="receiver", password="pass")


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


def test_send_coins(auth_client, mocker, receiver):
    mock_response = {"message": "Coins sent successfully"}
    mocker.patch("requests.post",
                 return_value=mocker.Mock(json=lambda: mock_response,
                                          status_code=200))

    response = auth_client.post("/api/sendCoin/",
                                {"toUser": receiver.username, "amount": 50},
                                format="json")
    assert response.status_code == 200
    assert response.json() == mock_response
