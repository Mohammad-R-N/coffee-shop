from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from utils import IsAdminUserMixin
from django.contrib import messages
from carts.forms import CartAddForm
from interactions.models import Comment
from interactions.forms import CommentCreateForm, CommentReplyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


class ProductDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, slug=kwargs["slug"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug):
        form = CartAddForm()
        comments = self.product_instance.pcomments.filter(is_reply=False)
        return render(
            request,
            "products/product-detail.html",
            {
                "product": self.product_instance,
                "form": form,
                "comments": comments,
                "comment_form": self.form_class,
                "reply_form": self.form_class_reply,
            },
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product_instance
            new_comment.save()
            messages.success(request, "your comment submitted successfully", "success")
            return redirect(
                "products:product-detail",
                self.product_instance.slug,
            )


class ProductAddReplyView(View):
    form_class = CommentReplyForm

    def post(self, request, product_id, comment_id):
        product = get_object_or_404(Product, id=product_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "your reply submitted successfully", "success")
        return redirect("products:product-detail", product.slug)


class BucketHome(IsAdminUserMixin, View):
    template_name = "products/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        p = Paginator(objects, 10)
        page = request.GET.get("page")
        objects = p.get_page(page)
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
