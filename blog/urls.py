from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.views import (NoteListView, NoteDetailView, NoteCreateView,
                        NoteDeleteView, NoteUpdateView)

app_name = 'blog'

urlpatterns = [
                  path('blog/', NoteListView.as_view(), name='list'),
                  path('blog/create/', NoteCreateView.as_view(),
                       name='create'),
                  path('blog/view/<int:pk>/', NoteDetailView.as_view(),
                       name='detail_view'),
                  path('blog/delete/<int:pk>', NoteDeleteView.as_view(),
                       name='delete'),
                  path('blog/edit/<int:pk>', NoteUpdateView.as_view(), name='edit'),
              ]
