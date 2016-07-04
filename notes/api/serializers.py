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

        print("#####################", validated_data)
        comments = validated_data.pop('comments')
        tags = validated_data.pop('tags')

        new_note = Note(**validated_data)
        new_note.save()

        for comment_data in comments:
            new_note.comments.append(Comment(**comment_data))

        print("----", tags)
        for tag_data in tags:
            print(tag_data['tag'])
            new_note.add_tag(tag_name=tag_data['tag'])
            #new_note.tags.append(Tag(**tag_data))

        new_note.save()
        return new_note





