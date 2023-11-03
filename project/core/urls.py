from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home-page"),
    path(
        "category/<slug:category_slug>/", views.HomeView.as_view(), name="category-slug"
    ),
]
