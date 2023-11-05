from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Order, OrderItem, Coupon
from .forms import CartAddForm, CouponApplyForm
from products.models import Product
from utils import Cart
import datetime
import requests
import json


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "carts/cart.html", {"cart": cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data["quantity"])
        return redirect("carts:cart")


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("carts:cart")


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(
            request, "carts/order.html", {"order": order, "form": self.form_class}
        )


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"],
            )
        cart.clear()
        return redirect("carts:order_detail", order.id)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            try:
                coupon = Coupon.objects.get(
                    code__exact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True,
                )
            except Coupon.DoesNotExist:
                messages.error(request, "this coupon does not exists", "danger")
                return redirect("carts:order_detail", order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect("carts:order_detail", order_id)


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8080/carts/verify/"


def send_request(request, order_id):
    order = Order.objects.get(id=order_id)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Description": description,
        "Phone": request.user.phone_number,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                return {
                    "status": True,
                    "url": ZP_API_STARTPAY + str(response["Authority"]),
                    "authority": response["Authority"],
                }
            else:
                return {"status": False, "code": str(response["Status"])}
        return response

    except requests.exceptions.Timeout:
        return {"status": False, "code": "timeout"}
    except requests.exceptions.ConnectionError:
        return {"status": False, "code": "connection error"}


def verify(authority):
    order = Order.objects.all()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response["Status"] == 100:
            return {"status": True, "RefID": response["RefID"]}
        else:
            return {"status": False, "code": str(response["Status"])}
    return response
