from django.conf.urls import url, include

from noteapp.views import IndexView
from notes.api.views import NoteList, NoteDetail, NoteDetailSlug
from notes.api.views import TagList, TagDetail

from authentication.api.views import (
    RegisterAccountView, AccountList, AccountDetail, LoginView, LogoutView)


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
    url(r'^register/$', RegisterAccountView.as_view(), name='account-register'),
]


urlpatterns = [
    url(r'^.*$', IndexView.as_view(), name='index'),

    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^api/v1/notes/', include(note_urls)),
    url(r'^api/v1/tags/', include(tag_urls)),
    url(r'^api/v1/account/', include(account_urls)),
    url(r'^api/v1/auth/login/', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/', LogoutView.as_view(), name='logout'),
]