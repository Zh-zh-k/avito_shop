import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import SendCoinSerializer


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = requests.get(f"{settings.AVITO_API_URL}/api/info",
                                headers={"Authorization": request.headers.get("Authorization")})
        return Response(response.json(), status=response.status_code)


class SendCoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendCoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = requests.post(f"{settings.AVITO_API_URL}/api/sendCoin",
                                 json=request.data,
                                 headers={"Authorization": request.headers.get("Authorization")})
        return Response(response.json(), status=response.status_code)


class BuyItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item):
        response = requests.get(f"{settings.AVITO_API_URL}/api/info",
                                headers={"Authorization": request.headers.get("Authorization")})
        user_data = response.json()
        coins = user_data.get("coins", 0)

        item_prices = {
            "t-shirt": 80, "cup": 20, "book": 50, "pen": 10, "powerbank": 200,
            "hoody": 300, "umbrella": 200, "socks": 10, "wallet": 50, "pink-hoody": 500
        }

        if item not in item_prices:
            return Response({"error": "Invalid item"}, status=400)

        if coins < item_prices[item]:
            return Response({"error": "Not enough coins"}, status=400)

        response = requests.get(f"{settings.AVITO_API_URL}/api/buy/{item}",
                                headers={"Authorization": request.headers.get("Authorization")})
        return Response(response.json(), status=response.status_code)


class AuthView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"},
                            status=400)

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.save()

        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token)}, status=200)
