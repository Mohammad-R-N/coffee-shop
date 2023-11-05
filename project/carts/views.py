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
