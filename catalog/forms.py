from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_current' or field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'

            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'price', 'preview',
                  'category')
    stop_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                  'бесплатно', 'обман', 'полиция', 'радар']

    def clean_product_name(self):
        nomination = self.cleaned_data['product_name']
        for word in self.stop_words:
            if word in nomination:
                raise forms.ValidationError(f'Выберите другой вариант'
                                            f' {self.stop_words}')
        return nomination

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in self.stop_words:
            if word in description:
                raise forms.ValidationError(f'Выберите другой вариант'
                                            f' {self.stop_words}')

        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

        name = forms.CharField(widget=forms.TextInput(
            attrs={"class": "myfield"}))


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published', )
