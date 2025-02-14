from django.urls import path

from .views import UserInfoView, SendCoinsView, BuyItemView, AuthView

app_name = 'api'

urlpatterns = [
    path("user/info/", UserInfoView.as_view(), name="user-info"),
    path("user/send-coins/", SendCoinsView.as_view(), name="send-coins"),
    path("user/buy/", BuyItemView.as_view(), name="buy-item"),
    path("auth/", AuthView.as_view(), name="auth"),
]
