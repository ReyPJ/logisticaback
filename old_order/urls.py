from django.urls import path
from .views import OldOrderRecieverAPIView, OldeOrderListAPIView

urlpatterns = [
    path('transfer-order/', OldOrderRecieverAPIView.as_view(),
         name='transfer-order-to-backup'),
    path('old-orders/', OldeOrderListAPIView.as_view(),
         name='old-orders-list-view'),
]
