from django.conf.urls import url, include

from notes import views
from notes.api.views import NoteList, NoteDetail, NoteDetailSlug
from notes.api.views import TagList, TagDetail

from authentication.api.views import (
    CreateAccountView, AccountList, AccountDetail)


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

account_urls = [
    url(r'^$', AccountList.as_view(), name='account-list'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/$',
        AccountDetail.as_view(), name='account-detail'),
    url(r'^register', CreateAccountView.as_view(), name='account-create')
]


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^api/v1/notes/', include(note_urls)),
    url(r'^api/v1/tags/', include(tag_urls)),
    url(r'^api/v1/account/', include(account_urls)),

]

