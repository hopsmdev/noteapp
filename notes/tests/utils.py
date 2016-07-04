from mongoengine.connection import connect, disconnect, get_connection
from django.test import TestCase
from notes.models import *
from noteapp.settings import test


class TestCaseMongo(TestCase):

    def _pre_setup(self):
        disconnect()
        connect(test.MONGODB_NAME)

    def _post_teardown(self):
        connection = get_connection()
        connection.drop_database(test.MONGODB_NAME)
        disconnect()


class TestDataFactory(object):

    def create_tags(self):
        self.tag_a = Tag(tag='a')
        self.tag_b = Tag(tag='b')
        self.tag_c = Tag(tag='c')

        self.tag_a.save()
        self.tag_b.save()
        self.tag_c.save()


    def create_comments(self):
        comment_1 = {"author": "Author1",
                     "email": "author1@test.com",
                     "text": "First comment of Author1"}

        comment_2 = {"author": "Author1",
                     "email": "author1@test.com",
                     "text": "Second comment of Author1"}

        comment_3 = {"author": "Author2",
                     "email": "author2@test.com",
                     "text": "First comment of Author2"}

        comment_4 = {"author": "Author2",
                     "email": "author2@test.com",
                     "text": "Second comment of Author2"}

        self.comment_auth1_1 = Comment(**comment_1)
        self.comment_auth1_2 = Comment(**comment_2)
        self.comment_auth2_1 = Comment(**comment_3)
        self.comment_auth2_2 = Comment(**comment_4)


    def create_notes(self):

        self.short_note = Note(
            title="test note",
            text="test note text",
            tags=[self.tag_a, self.tag_b],
            slug="short-note",
            comments=[
                self.comment_auth1_1,
                self.comment_auth1_2,
                self.comment_auth2_1])

        self.long_note = Note(
            title="test long note",
            text="".join(str(i) for i in range(0, 100)),
            tags=[self.tag_a, self.tag_b, self.tag_c],
            comments=[
                self.comment_auth1_1,
                self.comment_auth1_2,
                self.comment_auth2_1])

        self.note_noslug = Note(
            title="test noslug note",
            text="test noslug note text",
            tags=[self.tag_a, self.tag_b],)

        self.short_note.save()
        self.long_note.save()
        self.note_noslug.save()


    def data_setup(self):
        self.create_tags()
        self.create_comments()
        self.create_notes()



