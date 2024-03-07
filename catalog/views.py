import csv
import os
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from catalog.models import Product


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
    fields = ('product_name', 'description', 'price', 'preview', 'category', 'created_at', 'updated_at', 'avatar')
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'description', 'price', 'preview', 'category', 'created_at', 'updated_at', 'avatar')
    success_url = reverse_lazy('catalog:index')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

