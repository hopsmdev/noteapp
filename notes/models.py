import datetime
from django.utils.text import slugify
from bson.objectid import ObjectId
from mongoengine import Document, EmbeddedDocument, PULL
from mongoengine.fields import *

import logging
logger = logging.getLogger(__name__)


class Comment(EmbeddedDocument):
    _id = ObjectIdField(
        required=True, default=lambda: ObjectId(), primary_key=True)
    pub_date = DateTimeField(default=datetime.datetime.now, required=True)
    author = StringField(verbose_name="Author", max_length=255, required=True)
    email = EmailField(verbose_name="Email")
    text = StringField(verbose_name="Comment", required=True)

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


class Note(Document):
    pub_date = DateTimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=255, required=True)
    text = StringField(verbose_name="Text", required=True)
    comments = ListField(EmbeddedDocumentField('Comment'))
    slug = StringField(max_length=60)
    is_published = BooleanField(default=False)
    tags = ListField(ReferenceField(Tag, reverse_delete_rule=PULL))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-pub_date', 'slug'],
        'ordering': ['-pub_date']
    }

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:60]
        return super(Note, self).save(*args, **kwargs)

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

    def delete_tag(self, tag_name=None):

        tag = Tag.objects(tag=tag_name).first()
        if not tag:
            logger.debug(
                "Tag {} does not exist, cannot remove".format(tag_name))
            return

        Note.objects(id=self.id).update_one(
            pull__tags=Tag.objects(tag=tag_name).first())
        self.save()

    def delete_comment(self, comment_id=None):
        Note.objects(id=self.id).update_one(
            pull__comments={'_id': comment_id})
        self.save()

    def add_comment(self, comment):
        if comment:
            Note.objects(id=self.id).update_one(push__comments=comment)
            self.save()

    def add_tag(self, tag_name=None):

        tag = Tag.objects(tag=tag_name).first()
        if not tag:
            logger.debug(
                "Tag {} does not exist, create new one".format(tag_name))
            tag = Tag(tag=tag_name)
            tag.save()

        tag = Tag.objects(tag=tag_name).first()
        Note.objects(id=self.id).update_one(push__tags=tag)
        self.save()