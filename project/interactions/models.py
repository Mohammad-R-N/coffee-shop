from django.db import models
from products.models import Product
from accounts.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="pcomments"
    )
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="rcomments",
        blank=True,
        null=True,
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"
