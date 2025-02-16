from rest_framework import serializers


class SendCoinSerializer(serializers.Serializer):
    """ Сериализатор для отправки монет другому пользователю """
    toUser = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
