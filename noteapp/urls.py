"""noteapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from notes import views
from notes.api.views import NoteList, NoteDetail, NoteDetailSlug
from notes.api.views import TagList, TagDetail

note_urls = [
    url(r'^$', NoteList.as_view(), name='user-list'),
    url(r'^(?P<id>[0-9a-zA-Z]+)/$',
        NoteDetail.as_view(), name='note-detail'),
    url(r'^(?P<slug>[0-9a-zA-Z]+)/$',
        NoteDetailSlug.as_view(), name='note-detail-slug'),
]

tag_urls = [
    url(r'^$', TagList.as_view(), name='tag-list'),
    url(r'^(?P<tag>[0-9a-zA-Z]+)/$',
        TagDetail.as_view(), name='tag-detail')
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/notes/', include(note_urls)),
    url(r'^api/v1/tags/', include(tag_urls)),
]

