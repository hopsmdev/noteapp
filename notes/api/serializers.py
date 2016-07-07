import logging
from rest_framework.serializers import SerializerMethodField
from rest_framework_mongoengine.serializers import (
    DocumentSerializer, EmbeddedDocumentSerializer, drf_fields)
from notes.models import *
from rest_framework.reverse import reverse


class CommentSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Comment


class TagSerializer(DocumentSerializer):

    tag = drf_fields.CharField(max_length=128)

    class Meta:
        model = Tag


class NoteSerializer(DocumentSerializer):

    links = SerializerMethodField()

    comments = CommentSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note

    def create(self, validated_data):

        tags = validated_data.pop('tags')

        new_note = Note(**validated_data)
        new_note.tags.extend([(Tag(**tag_data)) for tag_data in tags])
        new_note.save()

        return new_note

    def update(self, instance, validated_data):

        tags = validated_data.pop('tags')
        comments = validated_data.pop('comments')

        updated_instance = super(NoteSerializer, self).update(
            instance, validated_data)
        tags = [(Tag(**tag_data)) for tag_data in tags]

        updated_instance.update(tags=tags, comments=comments)

        return updated_instance

    def get_links(self, obj):
        request = self.context['request']
        return {
            "self": reverse(
                'note-detail', kwargs={'id': obj.id}, request=request)
        }