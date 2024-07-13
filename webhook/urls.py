from django.urls import path
from .views import WebHookHandler, OrderList, OrderPrepared, OrderShipped, OrderDeleteView

urlpatterns = [
    path('webhook/', WebHookHandler.as_view(), name='webhookhandler'),
    path('orders/', OrderList.as_view(), name='orderlist'),
    path('orders/<int:order_id>/prepared/',
         OrderPrepared.as_view(), name='orderprepared'),
    path('orders/<int:order_id>/shipped/',
         OrderShipped.as_view(), name='ordershipped'),
    path('orders/<int:order_id>/delete/',
         OrderDeleteView.as_view(), name='orderdelete'),
]
