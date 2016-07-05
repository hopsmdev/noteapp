import logging
from rest_framework_mongoengine import fields
from rest_framework_mongoengine.serializers import (
    DocumentSerializer, EmbeddedDocumentSerializer, drf_fields)
from notes.models import *


class CommentSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Comment


class TagSerializer(DocumentSerializer):

    tag = drf_fields.CharField(max_length=128)

    class Meta:
        model = Tag


class NoteSerializer(DocumentSerializer):
    comments = CommentSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def create(self, validated_data):

        comments = validated_data.pop('comments')
        tags = validated_data.pop('tags')

        new_note = Note(**validated_data)

        new_note.tags.extend([(Tag(**tag_data)) for tag_data in tags])
        new_note.comments.extend([(Comment(**comment_data))
                                  for comment_data in comments])

        new_note.save()
        return new_note






