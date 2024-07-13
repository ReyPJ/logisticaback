from django.http import HttpResponseRedirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import OrderSerializer
from .models import Order
from old_order.models import Old_orders
from django.core.mail import send_mail
import json
import os
import logging

logger = logging.getLogger(__name__)


class WebHookHandler(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        try:
            payload = request.body
            payload_data = json.loads(payload)

            order_id = payload_data.get('id')
            order_total = payload_data.get('total')
            customer_name = payload_data.get(
                'billing', {}).get('first_name').upper()
            customer_last_name = payload_data.get(
                'billing', {}).get('last_name').upper()
            billing_address = json.dumps(payload_data.get('billing', {}))
            shipping_address = json.dumps(payload_data.get('shipping', {}))
            order_status = payload_data.get('status')
            payment_method = payload_data.get('payment_method')
            customer_note = payload_data.get('customer_note', '')

            line_items = payload_data.get('line_items', [])
            shipping_lines = payload_data.get('shipping_lines', [])

            order, created = Order.objects.update_or_create(
                order_id=order_id,
                defaults={
                    'order_total': order_total,
                    'customer_name': customer_name,
                    'customer_last_name': customer_last_name,
                    'billing_address': billing_address,
                    'shipping_address': shipping_address,
                    'order_status': order_status,
                    'payment_method': payment_method,
                    'customer_note': customer_note,
                    'item': line_items,
                    'shipping_lines': shipping_lines
                }
            )

            return Response({'status': 'success', 'message': 'WebHook recibido y procesado correctamente'})

        except json.JSONDecodeError as e:
            logger.error(f'Error en el JSON: {str(e)}')
            return Response({'status': 'error', 'message': 'Error en el JSON'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'Error en el WebHook: {str(e)}')
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', 'new')
        return Order.objects.filter(status=status)


class OrderPrepared(APIView):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(order_id=order_id)
            order.mark_as_prepared()
            return Response({'status': 'success', 'message': 'Orden marcada como preparada'}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response({'status': 'error', 'message': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, order_id, *args, **kwargs):
        return self.post(request, order_id, *args, **kwargs)


class OrderShipped(APIView):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(order_id=order_id)
            order.mark_as_shipped()

            subject = 'Notificación de envío de pedido'
            message = f'El pedido {order_id} ha sido enviado.'
            send_mail(
                subject,
                message,
                None,
                ['reynerjiemenz@gmail.com', 'reyner1012002@gmail.com'],
                fail_silently=False,
            )

            return Response({'status': 'success', 'message': 'Orden marcada como preparada'}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response({'status': 'error', 'message': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, order_id, *args, **kwargs):
        return self.post(request, order_id, *args, **kwargs)


class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'status': 'error', 'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.status != 'shipped':
            return Response({'status': 'error', 'message': 'Order is not shipped yet so it can not be deleted'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            old_order = Old_orders.objects.get(order_id=order_id)
        except Old_orders.DoesNotExist:
            return Response({'status': 'error', 'message': 'The order is not saved yet'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({'status': 'success', 'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
