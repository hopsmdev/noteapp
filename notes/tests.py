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

        self.tag_a = Tag(tag='a')
        self.tag_b = Tag(tag='b')
        self.tag_c = Tag(tag='c')

        self.tag_a.save()
        self.tag_b.save()
        self.tag_c.save()

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
        self.assertEqual(self.note_noslug.slug, correct_slug)

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

    def test_delete_note(self):

        self.short_note.save()
        self.long_note.save()
        self.note_noslug.save()

        notes = Note.objects()
        self.assertEqual(len(notes), 3)

        self.note_noslug.delete()
        notes = Note.objects()
        self.assertEqual(len(notes), 2)

    def test_delete_comment_from_note(self):

        self.short_note.save()
        note = Note.objects(slug="short-note").first()
        comment_ids = [comment._id for comment in note.comments]
        self.assertEqual(len(comment_ids), 3)

        comment_to_remove = comment_ids[0]

        Note.objects(slug="short-note").update_one(
            pull__comments={'_id': comment_to_remove})

        note.reload()
        comment_ids = [comment._id for comment in note.comments]
        self.assertEqual(len(comment_ids), 2)

    def test_delete_note_comment(self):

        self.short_note.save()
        note = Note.objects(slug="short-note").first()
        comment_ids = [comment._id for comment in note.comments]
        self.assertEqual(len(comment_ids), 3)
        comment_to_remove = comment_ids[0]

        self.short_note.delete_comment(comment_to_remove)

        note.reload()
        comment_ids = [comment._id for comment in note.comments]
        self.assertEqual(len(comment_ids), 2)

    def test_delete_tag_from_note(self):

        self.short_note.save()
        note = Note.objects(slug="short-note").first()
        note_tags = [tag.tag for tag in note.tags]
        self.assertEqual(len(note_tags), 2)

        tag_to_remove = self.tag_a

        Note.objects(slug="short-note").update_one(
            pull__tags=tag_to_remove)

        note.reload()
        note_tags = [tag.tag for tag in note.tags]
        self.assertEqual(len(note_tags), 1)

        # confirm that we only unset tag from note - we do not want to remove
        # tag from db
        self.assertTrue(Tag.objects(tag='a'))

    def test_delete_tag_from_note_using_tag_name(self):

        self.short_note.save()
        self.short_note.delete_tag(tag_name='a')
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]
        self.assertEqual(len(note_tags), 1)

    def test_delete_notexisting_tag_from_note(self):

        self.short_note.save()
        self.short_note.delete_tag(tag_name='XX')
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]
        self.assertEqual(len(note_tags), 2)

    def test_delete_tag(self):

        self.short_note.save()  # note taged with 2 tags: a and b
        note = Note.objects(slug='short-note').first()
        self.assertEqual(len(note.tags), 2)

        tags = Tag.objects()
        self.assertEqual(len(tags), 3)
        self.tag_a.delete()

        tags = Tag.objects()
        self.assertEqual(len(tags), 2)

        # confirm that tag was also removed from Note

        note = Note.objects(slug='short-note').first()
        self.assertEqual(len(note.tags), 1)

    def test_add_comment(self):

        self.short_note.save()
        note = Note.objects(slug="short-note").first()
        self.assertEqual(len(note.comments), 3)

        self.short_note.add_comment(self.comment_auth2_2)

        note.reload()
        self.assertEqual(len(note.comments), 4)

    def test_add_tag_to_note(self):

        new_tag = "c"

        self.short_note.save()
        self.short_note.add_tag(tag_name=new_tag)
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]
        self.assertEqual(len(note_tags), 3)

        tag = Tag.objects(tag=new_tag).first()
        self.assertEqual(tag.tag, new_tag)

    def test_add_notexisting_tag_to_note(self):

        new_tag = "NEWTAG"

        self.short_note.save()
        self.short_note.add_tag(tag_name=new_tag)
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]
        self.assertEqual(len(note_tags), 3)

        tag = Tag.objects(tag=new_tag).first()
        self.assertEqual(tag.tag, new_tag)