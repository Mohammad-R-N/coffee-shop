from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from utils import IsAdminUserMixin
from django.contrib import messages
from carts.forms import CartAddForm


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(
            request, "products/product-detail.html", {"product": product, "form": form}
        )

    def post(self, request):
        pass


class BucketHome(IsAdminUserMixin, View):
    template_name = "products/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {"objects": objects})


class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, "your object will be delete soon.", "info")
        return redirect("products:bucket")


class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, "your download will start soon.", "info")
        return redirect("products:bucket")
