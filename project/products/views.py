from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from utils import IsAdminUserMixin
from django.contrib import messages


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, "products/product-detail.html", {"product": product})

    def post(self, request):
        pass
