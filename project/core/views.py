from django.shortcuts import render
from django.views import View
from products.models import Category, Product


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(
            request,
            "core/home-page.html",
            {"products": products, "categories": categories},
        )
