from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'api/info', UserViewSet, basename='user_info')
router.register(r'api/sendCoin', UserViewSet, basename='send_coin')
router.register(r'api/buy', UserViewSet, basename='buy_item')
router.register(r"api/user", UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt'))
]
