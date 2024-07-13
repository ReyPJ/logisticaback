from django.db import models


class Order(models.Model):
    order_id = models.IntegerField(unique=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=255)
    customer_last_name = models.CharField(
        max_length=255, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    customer_note = models.TextField(blank=True, null=True)
    item = models.JSONField(default=list)
    shipping_lines = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('new', 'Nueva Orden'),
        ('prepared', 'Lista para enviar'),
        ('shipped', 'Enviada')
    ]

    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='new'
    )

    def mark_as_prepared(self):
        self.status = 'prepared'
        self.save()

    def mark_as_shipped(self):
        self.status = 'shipped'
        self.save()

    def __str__(self):
        return f'Orden: {self.order_id} - Cliente: {self.customer_name}'
