from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from utils import Cart
from .forms import CartAddForm, CouponApplyForm
from products.models import Product
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
import datetime
from django.contrib import messages


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
