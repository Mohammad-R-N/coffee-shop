from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from products.models import Product
from utils import phone_number_validator, PhoneNumberField
from accounts.models import User


class Cart(models.Model):
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    total_quantity = models.PositiveIntegerField()
    customer_number = PhoneNumberField(
        _("phone number"), max_length=14, validators=[phone_number_validator]
    )
    user_cart = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.total_quantity} order "


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.price} - {self.quantity} "
