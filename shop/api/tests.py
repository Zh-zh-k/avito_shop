from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import requests
from unittest.mock import patch


class AvitoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.token = "testtoken"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @patch("requests.post")
    def test_auth_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"token": self.token}

        response = self.client.post("/api/auth",
                                    {"username": self.username,
                                     "password": self.password},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    @patch("requests.get")
    def test_get_wallet_info(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "coins": 1000,
            "inventory": [{"type": "t-shirt", "quantity": 1}],
            "coinHistory": {"received": [], "sent": []}
        }

        response = self.client.get("/api/info")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["coins"], 1000)
        self.assertEqual(response.data["inventory"][0]["type"], "t-shirt")

    @patch("requests.post")
    def test_send_coin_success(self, mock_post):
        mock_post.return_value.status_code = 200

        response = self.client.post("/api/sendCoin",
                                    {"toUser": "user2", "amount": 50},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("requests.get")
    def test_buy_item_success(self, mock_get):
        mock_get.return_value.status_code = 200

        response = self.client.get("/api/buy/t-shirt")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("requests.get")
    def test_buy_item_not_enough_coins(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {
            "errors": "Not enough coins"
            }

        response = self.client.get("/api/buy/hoody")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"], "Not enough coins")
