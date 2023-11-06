from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control bg-light text-dark",
                    "style": "height: 170px; width: 60%;",
                    "placeholder": "NEW COMMENT...",
                }
            )
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control bg-light",
                    "style": "height: 100px; width: 40%;",
                    "placeholder": "ANSWER...",
                }
            )
        }
