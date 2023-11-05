from django.shortcuts import render
from django.views import View
from products.models import Category, Product
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


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


class SearchProducts(View):
    def get(self, request):
        result = request.GET.get("searchbox")
        products = Product.objects.all()
        if result:
            products = (
                products.annotate(
                    similarity=TrigramSimilarity("name", str(result)),
                )
                .filter(similarity__gt=0.3)
                .order_by("-similarity")
            )

        return render(request, "core/search_results.html", {"results": products})
