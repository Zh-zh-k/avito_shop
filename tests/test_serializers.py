import pytest
from shop.api.serializers import SendCoinSerializer


@pytest.mark.parametrize("data, is_valid", [
    ({"toUser": "alice", "amount": 10}, True),
    ({"toUser": "bob", "amount": 0}, False),
    ({"toUser": "", "amount": 10}, False),
])
def test_send_coin_serializer(data, is_valid):
    serializer = SendCoinSerializer(data=data)
    assert serializer.is_valid() == is_valid
