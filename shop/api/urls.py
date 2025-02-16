from django.urls import path
from .views import UserInfoView, SendCoinView, BuyItemView, AuthView

urlpatterns = [
    path("api/info/", UserInfoView.as_view(), name="user_info"),
    path("api/sendCoin/", SendCoinView.as_view(), name="send_coin"),
    path("api/buy/<str:item>/", BuyItemView.as_view(), name="buy_item"),
    path("api/auth/", AuthView.as_view(), name="auth"),
]
