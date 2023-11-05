from kavenegar import *
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.mixins import UserPassesTestMixin
from products.models import Product


def send_otp(phone_number, code):
    try:
        API_KEY = "35484F79694A68527A58302F43354176354C366A62552B37665942646F334439627179326F564E766E63413D"
        api = KavenegarAPI(f"https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json")
        params = {
            "sender": "",
            "receptor": phone_number,
            "token": code,
            "template": "maktab",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def phone_number_validator(value):
    """
    Validates phone numbers in the 09XX, 00989XX, or +98XX format and replaces the +98 and 0098 parts with 0.
    """
    phone_regex = r"^(\+98|0098|0)?9\d{9}$"
    if not re.match(phone_regex, value):
        raise ValidationError(
            "Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."
        )
    formatted_phone_number = re.sub(r"^\+98|^0098", "0", value)
    return formatted_phone_number


class PhoneNumberField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            regex = phone_number_validator(value)
        except ValidationError:
            raise ValidationError(
                "Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."
            )

        formatted_phone_number = re.sub(r"^\+98|^0098", "0", value)
        return formatted_phone_number


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["total_price"] = int(item["price"]) * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item["price"]) * item["quantity"] for item in self.cart.values())

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
