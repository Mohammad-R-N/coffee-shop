from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created", "is_reply")
    raw_id_fields = ("user", "product", "reply")
