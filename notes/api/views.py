from rest_framework import permissions, generics
from rest_framework_mongoengine import generics as mongo_generics

from .serializers import NoteSerializer, TagSerializer
from notes.models import Note, Tag


class NoteList(mongo_generics.ListCreateAPIView):
    model = Note
    queryset = Note.objects()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]


class NoteDetail(mongo_generics.RetrieveUpdateDestroyAPIView):
    model = Note
    queryset = Note.objects()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class NoteDetailSlug(NoteDetail):
    lookup_field = 'slug'


class TagList(mongo_generics.ListCreateAPIView):
    model = Tag
    queryset = Tag.objects()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagDetail(mongo_generics.RetrieveUpdateDestroyAPIView):
    model = Tag
    queryset = Tag.objects()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'tag'





