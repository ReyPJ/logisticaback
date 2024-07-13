from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import Old_ordersSerializer
from .models import Old_orders
from webhook.models import Order
import json
import os


class OldOrderRecieverAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'status': 'error', 'message': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'status': 'error', 'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        old_order_data = {
            "order_id": order.order_id,
            "order_total": order.order_total,
            "customer_name": order.customer_name,
            "customer_last_name": order.customer_last_name,
            "billing_address": order.billing_address,
            "shipping_address": order.shipping_address,
            "order_status": order.order_status,
            "payment_method": order.payment_method,
            "customer_note": order.customer_note,
            "item": order.item,
            "shipping_lines": order.shipping_lines,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "status": "shipped",
        }

        old_order_serializer = Old_ordersSerializer(data=old_order_data)
        if old_order_serializer.is_valid():
            old_order_serializer.save()
            return Response({'status': 'success', 'message': 'Old Order created successfully'}, status=status.HTTP_201_CREATED)
        return Response(old_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OldeOrderListAPIView(generics.ListAPIView):
    queryset = Old_orders.objects.all()
    serializer_class = Old_ordersSerializer
    permission_classes = [AllowAny]
