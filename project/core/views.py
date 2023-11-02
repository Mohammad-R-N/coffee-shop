from django.shortcuts import render
from django.views import View
from products.models import Category, Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, "core/home-page.html", {"products": products})
