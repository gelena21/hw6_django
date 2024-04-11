from django import forms

from blog.models import Note


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        exclude = 'slug', 'views_count'
