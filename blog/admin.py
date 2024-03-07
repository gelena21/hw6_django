from django.contrib import admin

from blog.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("header", "is_published",)

# Register your models here.
