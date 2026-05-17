from django import forms
from django.contrib.auth.forms import AuthenticationForm

from content.models import NewsItem, Retreat


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class BaseStyledModelForm(forms.ModelForm):
    textareas = {"excerpt", "body", "description"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            classes = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                classes = "form-checkbox"
            elif isinstance(field.widget, forms.ClearableFileInput):
                classes = "form-file"
            elif name in self.textareas:
                field.widget.attrs.setdefault("rows", 5)
            field.widget.attrs.update({"class": classes})


class NewsItemForm(BaseStyledModelForm):
    published_at = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Fecha",
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = NewsItem
        fields = [
            "title",
            "image",
            "excerpt",
            "body",
            "published_at",
            "order",
            "show_on_home",
            "is_active",
        ]


class RetreatForm(BaseStyledModelForm):
    class Meta:
        model = Retreat
        fields = [
            "title",
            "description",
            "body",
            "image",
            "signup_url",
            "is_featured",
            "order",
            "is_active",
        ]
