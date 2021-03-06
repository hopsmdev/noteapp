import datetime
from django.utils.text import slugify
from bson.objectid import ObjectId
from django_mongoengine import Document, EmbeddedDocument
from django_mongoengine.fields import *
from mongoengine import PULL

import logging
logger = logging.getLogger(__name__)


class Comment(EmbeddedDocument):
    _id = ObjectIdField(
        required=True, default=lambda: ObjectId(), primary_key=True)
    pub_date = DateTimeField(default=datetime.datetime.now, required=True)
    author = StringField(verbose_name="Author", max_length=255,
                         required=True, blank=True)
    email = EmailField(verbose_name="Email", blank=True)
    text = StringField(verbose_name="Comment", required=True, blank=True)

    def short_text(self):
        return ' '.join(self.text.split()[:20]) + " ..."  \
            if len(self.text) > 20 else self.text

    def __str__(self):
        return "{} on {}".format(
            self.author, self.pub_date.strftime('%Y-%m-%d'))


class Tag(Document):

    tag = StringField(
        max_length=128, required=True, primary_key=True, unique=True)

    def __str__(self):
        return str(self.tag)

    def __eq__(self, other):
        return isinstance(other, Tag) and self.tag == other.tag

    def __hash__(self):
        return hash(self.tag)


class Note(Document):
    pub_date = DateTimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=255, required=True)
    text = StringField(verbose_name="Text", required=True)
    comments = ListField(EmbeddedDocumentField('Comment'), blank=True)
    slug = StringField(max_length=60, blank=True)
    is_published = BooleanField(default=False, blank=True)
    tags = ListField(ReferenceField(Tag, reverse_delete_rule=PULL), blank=True)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-pub_date', 'slug'],
        'ordering': ['-pub_date']
    }

    @staticmethod
    def __is_iterable(arg):
        if not isinstance(arg, list):
           raise TypeError()

    @staticmethod
    def __add_tags(tags):

        if not tags:
            return []

        if not isinstance(tags, list):
            raise TypeError()

        for tag_obj in tags:
            _tag = Tag.objects(tag=tag_obj.tag).first()
            if not _tag:
                Tag(tag=tag_obj.tag).save().reload()
        return tags

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)[:60]

        kwargs['tags'] = self.__add_tags(tags=kwargs.get('tags'))
        kwargs['slug'] = self.slug

        return super(Note, self).save(*args, **kwargs)

    def update(self, **kwargs):

        update_dict = {}

        tags = kwargs.pop('tags', None)
        if tags and not set(tags).issubset(set(self.tags)):
            update_dict['push_all__tags'] = self.__add_tags(tags)

        comments = kwargs.pop('comments', None)
        if comments:
            update_dict['push_all__comments'] = comments

        for kwarg in kwargs:
            if kwarg in Note._fields.keys():
                update_dict['set__{}'.format(kwarg)] = kwargs.get(kwarg)

        if update_dict:
            return super(Note, self).update(**update_dict)

    def remove(self, **kwargs):

        remove_dict = {}

        tags = kwargs.pop('tags', None)
        if tags:
            remove_dict['pull_all__tags'] = tags

        comments = kwargs.pop('comments', None)
        if comments:
            remove_dict['pull_all__comments'] = comments

        for kwarg in kwargs:
            if kwarg in Note._fields.keys():
                remove_dict['unset__{}'.format(kwarg)] = kwargs.get(kwarg)

        if remove_dict:
            return super(Note, self).update(**remove_dict)

    def formatted_title(self):
        return self.title.title()

    def short_text(self):
        return ' '.join(self.text.split()[:20]) + " ..."  \
            if len(self.text) > 20 else self.text

    def get_slug(self):
        return self.slug

    def __str__(self):
        return "{} on {}".format(
            self.title, self.pub_date.strftime('%Y-%m-%d'))