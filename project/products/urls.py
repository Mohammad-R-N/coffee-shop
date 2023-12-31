from django.urls import path, include
from . import views

app_name = "products"

bucket_urls = [
    path("", views.BucketHome.as_view(), name="bucket"),
    path(
        "delete_obj/<str:key>/",
        views.DeleteBucketObject.as_view(),
        name="delete_obj_bucket",
    ),
    path(
        "download_obj/<str:key>/",
        views.DownloadBucketObject.as_view(),
        name="download_obj_bucket",
    ),
]


urlpatterns = [
    path("bucket/", include(bucket_urls)),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    path(
        "reply/<int:product_id>/<int:comment_id>/",
        views.ProductAddReplyView.as_view(),
        name="add_reply",
    ),
]
