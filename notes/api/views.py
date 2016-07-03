from rest_framework import generics, permissions


from .serializers import NoteSerializer, TagSerializer, CommentSerializer
from notes.models import Note, Tag, Comment


class NoteList(generics.ListCreateAPIView):
    model = Note
    queryset = Note.objects()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]


class TagList(generics.ListCreateAPIView):
    model = Tag
    queryset = Tag.objects()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]



