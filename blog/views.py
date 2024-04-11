from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, ListView, DetailView, DeleteView, UpdateView)
from pytils.translit import slugify
from blog.forms import BlogForm
from blog.models import Note


class NoteCreateView(CreateView):
    model = Note
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.header)
            new_note.save()

        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.header)
            new_note.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail_view', args=[self.kwargs.get('pk')])


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('blog:list')


class NoteListView(ListView):
    model = Note

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class NoteDetailView(DetailView):
    model = Note

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        return self.object
