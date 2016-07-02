from mongoengine.connection import connect, disconnect, get_connection, get_db
from django.test import TestCase
from notes.models import *
from noteapp.settings import test


class NoteModelTest(TestCase):

    def _pre_setup(self):
        disconnect()
        connect(test.MONGODB_NAME)
        #print('Creating mongo test database ' + test.MONGODB_NAME)

    def _post_teardown(self):
        connection = get_connection()
        connection.drop_database(test.MONGODB_NAME)
        #print('Dropping mongo test database: ' + test.MONGODB_NAME)
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

        self.note_noslug = Note(
            title="test noslug note",
            text="test noslug note text",
            tags=['a', 'b'])

    def test_string_repr(self):
        self.assertEqual(
            str(self.short_note),
            "{} on {}".format(
                self.short_note.title,
                self.short_note.pub_date.strftime('%Y-%m-%d')))

    def test_save_notes(self):
        self.short_note.save()
        note = Note.objects(slug="short-note").first()
        self.assertEqual(note.slug, 'short-note')

    def test_note_noslug(self):
        correct_slug = "test-noslug-note"
        self.note_noslug.save()
        self.assertEqual(self.note_noslug.get_slug(), correct_slug)
        self.assertEqual(self.note_noslug.id, correct_slug)

        note = Note.objects(title__contains="noslug").first()
        self.assertEqual(note.slug, correct_slug)

    def test_tags_exists(self):
        self.short_note.save()
        self.long_note.save()
        self.note_noslug.save()

        notes = Note.objects(tags__in='a')
        self.assertEqual(len(notes), 3)

        notes = Note.objects(tags__in='c')
        self.assertEqual(len(notes), 1)

    def test_tags_notexist(self):
        notes = Note.objects(tags__in='x')
        self.assertEqual(len(notes), 0)

    def test_get_Author1_comments(self):
        self.short_note.save()
        self.long_note.save()
        self.note_noslug.save()

        notes = Note.objects(comments__author="Author1")
        self.assertEqual(len(notes), 2)

        comments = [comment.email for note in notes for comment in note.comments
                    if comment.author == "Author1"]
        self.assertEqual(str(list(set(comments))[0]), "author1@test.com")
