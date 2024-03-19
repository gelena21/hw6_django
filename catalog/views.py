import csv
import os
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from catalog.models import Product
from catalog.forms import ProductForm, VersionForm
from django.forms import inlineformset_factory


def index(request):
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('data.csv', 'a', newline='') as file:
            fieldnames = ['Date', 'Name', 'Phone', 'Message']
            data = csv.DictWriter(file, fieldnames=fieldnames)
            file_empty = os.stat('data.csv').st_size == 0
            if file_empty:
                data.writeheader()
            data.writerow({'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Name': name, 'Phone': phone,
                           'Message': message})
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    context = {'object': Product.objects.get(pk=pk)}

    return render(request, 'catalog/product_detail.html', context)


def product_list(request):
    context = {'object_list': Product.objects.all()}

    return render(request, 'catalog/product_list.html', context)


class ProductView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    fields = ('product_name', 'description', 'price', 'preview', 'category', 'created_at', 'updated_at', 'avatar')
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'description', 'price', 'preview', 'category', 'created_at', 'updated_at', 'avatar')
    success_url = reverse_lazy('catalog:index')
    form_class = ProductForm

    def get_success_url(self, *args, **kwargs):
        return reverse("catalog:update_product", args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
