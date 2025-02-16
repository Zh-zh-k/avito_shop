from rest_framework import serializers


class SendCoinSerializer(serializers.Serializer):
    """
    Сериализатор для отправки монет другому пользователю
    (для валидации входных данных)
    """
    toUser = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
