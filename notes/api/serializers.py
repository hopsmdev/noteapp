from rest_framework_mongoengine.serializers import (
    DocumentSerializer, EmbeddedDocumentSerializer)
from notes.models import *


class CommentSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Comment


class TagSerializer(DocumentSerializer):
    class Meta:
        model = Tag


class NoteSerializer(DocumentSerializer):
    comments = CommentSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        depth = 2
        allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')






