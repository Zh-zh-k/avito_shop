import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedWithToken


class UserInfoView(APIView):
    """ Получение баланса, инвентаря и истории транзакций """
    permission_classes = [IsAuthenticatedWithToken]

    def get(self, request):
        token = request.headers.get("Authorization")
        headers = {"Authorization": token}
        response = requests.get(f"{settings.AVITO_API_URL}/api/info",
                                headers=headers)

        if response.status_code == 200:
            return Response(response.json())
        return Response(response.json(), status=response.status_code)


class SendCoinsView(APIView):
    """ Передача монет другому пользователю """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        headers = {"Authorization": f"Bearer {token}"}
        data = request.data

        response = requests.post(
            f"{settings.AVITO_API_URL}/api/sendCoin",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            return Response({"message": "Монеты успешно отправлены!"})
        return Response(response.json(), status=response.status_code)


class BuyItemView(APIView):
    """ Покупка товара за монеты """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        item = request.data.get("item")

        if not item:
            return Response({"error": "Укажите товар!"}, status=400)

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{settings.AVITO_API_URL}/api/buy/{item}",
                                headers=headers)

        if response.status_code == 200:
            return Response({"message": f"Товар '{item}' куплен!"})
        return Response(response.json(), status=response.status_code)


class AuthView(APIView):
    """ Аутентификация и получение JWT-токена """

    def post(self, request):
        data = request.data

        response = requests.post(f"{settings.AVITO_API_URL}/api/auth",
                                 json=data)

        if response.status_code == 200:
            return Response(response.json())
        return Response(response.json(), status=response.status_code)
