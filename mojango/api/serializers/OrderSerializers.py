from rest_framework import serializers

from ..models import Order


class OrderCreateSerializer(serializers.ModelSerializer):

    description = serializers.CharField(max_length=2000)

    class Meta:
        model = Order
        exclude = ['purchased_at', 'status']
