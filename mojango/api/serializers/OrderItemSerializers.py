from rest_framework import serializers

from ..models import OrderItem


class OrderItemCreateSerializer(serializers.ModelSerializer):

    amount = serializers.IntegerField(min_value=0)

    class Meta:
        model = OrderItem
        fields = "__all__"
