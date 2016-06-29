import datetime
from django.core.urlresolvers import reverse
from mongoengine import Document, EmbeddedDocument, fields


class Comment(EmbeddedDocument):
    pub_date = fields.DateTimeField(
        default=datetime.datetime.now, required=True)
    author = fields.StringField(verbose_name="Author",
                                max_length=255, required=True)
    email = fields.EmailField(verbose_name="Email")
    text = fields.StringField(verbose_name="Comment", required=True)

    def __str__(self):
        return "{} on {}".format(
            self.author, self.pub_date.strftime('%Y-%m-%d'))


class Note(Document):
    pub_date = fields.DateTimeField(
        default=datetime.datetime.now, required=True)
    title = fields.StringField(max_length=255, required=True)
    slug = fields.StringField(max_length=255, required=True, primary_key=True)
    comments = fields.ListField(fields.EmbeddedDocumentField('Comment'))
    text = fields.StringField(verbose_name="Text", required=True)
    tags = fields.ListField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-pub_date', 'slug'],
        'ordering': ['-pub_date']
    }

    def get_absolute_url(self):
        return reverse('note', kwargs={"slug": self.slug})

    def formatted_title(self):
        return self.title.title()

    def short_text(self):
        if len(self.text) > 20:
            return ' '.join(self.text.split()[:20]) + " ..."
        return self.text

    def __str__(self):
        return "{} on {}".format(
            self.title, self.pub_date.strftime('%Y-%m-%d'))