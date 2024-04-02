import csv
import os
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from catalog.models import Product, Version
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

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


class ProductView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for product in context['object_list']:
            product.active_version = product.version_set.filter(is_current=True).first()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    #fields = ('product_name', 'description', 'price', 'preview', 'category', 'created_at', 'updated_at', 'avatar')
    success_url = reverse_lazy('catalog:index')
    permission_required = "catalog.change_product"
    form_class = ProductForm

    def get_form_class(self):
        if self.request.user.is_staff:
            return ProductModeratorForm
        else:
            return ProductForm

    def test_func(self):
        user = self.request.user
        instance: Product = self.get_object()
        custom_perms: tuple = (
            'catalog.set_publication',
            'catalog.set_category',
            'catalog.set_description',
        )

        if user == instance.user:
            return True
        elif user.groups.filter(name='moderator') and user.has_perms(custom_perms):
            return True

        return self.handle_no_permission()

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.object.author != self.request.user and not self.request.user.is_staff:
            raise Http404("Доступа нет")

        return self.object

    def get_success_url(self, *args, **kwargs):
        return reverse("catalog:update_product", args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
