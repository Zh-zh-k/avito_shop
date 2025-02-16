import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SendCoinSerializer
from .permissions import IsAuthenticatedWithToken


class UserViewSet(ViewSet):
    """
    ViewSet для работы с информацией пользователя:
    - Получение баланса монет, истории транзакций и инвентаря
    - Передача монет другому пользователю
    - Покупка товаров
    """
    permission_classes = [IsAuthenticatedWithToken]

    def get_headers(self, request):
        """ Возвращает заголовки с токеном пользователя """
        return {"Authorization": request.headers.get("Authorization")}

    def list(self, request):
        """
        Получить информацию о пользователе (баланс, инвентарь, история
        транзакций)
        """
        response = requests.get(f"{settings.AVITO_API_URL}/api/info",
                                headers=self.get_headers(request))
        return Response(response.json(), status=response.status_code)

    @action(detail=False, methods=["post"])
    def send_coin(self, request):
        """ Передать монеты другому пользователю """
        serializer = SendCoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = requests.post(f"{settings.AVITO_API_URL}/api/sendCoin",
                                 headers=self.get_headers(request))
        return Response(response.json(), status=response.status_code)

    @action(detail=True, methods=["get"])
    def buy(self, request, pk=None):
        """ Купить товар по его названию (pk - это название товара) """
        response = requests.get(f"{settings.AVITO_API_URL}/api/buy/{pk}",
                                headers=self.get_headers(request))
        return Response(response.json(), status=response.status_code)

    @action(detail=False, methods=["post"], url_path="auth",
            permission_classes=[])
    def auth(self, request):
        """
        Авторизация пользователя с автоматическим созданием
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"},
                            status=400)

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.save()

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
