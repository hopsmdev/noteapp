from mongoengine.connection import connect, disconnect, get_connection, get_db
from django.test import TestCase
from notes.models import *
from noteapp.settings import test


class NoteModelTest(TestCase):

    def _pre_setup(self):
        disconnect()
        connect(test.MONGODB_NAME)
        print('Creating mongo test database ' + test.MONGODB_NAME)

    def _post_teardown(self):
        connection = get_connection()
        connection.drop_database(test.MONGODB_NAME)
        print('Dropping mongo test database: ' + test.MONGODB_NAME)
        disconnect()

    def setUp(self):

        self.comment_auth1_1 = Comment(
            author="Author1",
            email="author1@test.com",
            text="First comment of Author1")

        self.comment_auth1_2 = Comment(
            author="Author1",
            email="author1@test.com",
            text="Second comment of Author1")

        self.comment_auth2_1 = Comment(
            author="Author2",
            email="author2@test.com",
            text="First comment of Author2")

        self.short_note = Note(
            title="test note",
            text="test note text",
            tags=['a', 'b'],
            slug="short-note",
            comments=[
                self.comment_auth1_1,
                self.comment_auth1_2,
                self.comment_auth2_1])

        self.long_note = Note(
            title="test long note",
            text="".join(str(i) for i in range(0, 100)),
            tags=['a', 'b', 'c'],
            comments=[
                self.comment_auth1_1,
                self.comment_auth1_2,
                self.comment_auth2_1])



    def test_string_repr(self):
        self.assertEqual(
            str(self.short_note),
            "{} on {}".format(
                self.short_note.title,
                self.short_note.pub_date.strftime('%Y-%m-%d')))

    def test_save_notes(self):
        self.short_note.save()