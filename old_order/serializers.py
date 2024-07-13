from rest_framework import serializers
from .models import Old_orders


class Old_ordersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Old_orders
        fields = '__all__'
