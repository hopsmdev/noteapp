from notes.models import *
from notes.tests.utils import TestCaseMongo, TestDataFactory


class NoteModelTest(TestCaseMongo, TestDataFactory):

    def setUp(self):
        self.data_setup()

    def test_string_repr(self):

        self.assertEqual(
            str(self.short_note),
            "{} on {}".format(
                self.short_note.title,
                self.short_note.pub_date.strftime('%Y-%m-%d')))

    def test_save_notes(self):

        note = Note.objects(slug="short-note").first()
        self.assertEqual(note.slug, 'short-note')

    def test_note_noslug(self):

        correct_slug = "test-noslug-note"
        self.assertEqual(self.note_noslug.get_slug(), correct_slug)
        self.assertEqual(self.note_noslug.slug, correct_slug)

        note = Note.objects(title__contains="noslug").first()
        self.assertEqual(note.slug, correct_slug)

    def test_tags_exists(self):

        notes = Note.objects(tags__in='a')
        self.assertEqual(len(notes), 3)

        notes = Note.objects(tags__in='c')
        self.assertEqual(len(notes), 1)

    def test_tags_notexist(self):

        notes = Note.objects(tags__in='x')
        self.assertEqual(len(notes), 0)

    def test_get_Author1_comments(self):

        notes = Note.objects(comments__author="Author1")
        self.assertEqual(len(notes), 2)

        comments = [comment.email for note in notes for comment in note.comments
                    if comment.author == "Author1"]
        self.assertEqual(str(list(set(comments))[0]), "author1@test.com")

    def test_delete_note(self):

        notes = Note.objects()
        self.assertEqual(len(notes), 3)

        self.note_noslug.delete()
        notes = Note.objects()
        self.assertEqual(len(notes), 2)

    def test_delete_comment_from_note(self):

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

        self.short_note.remove(comments=[self.comment_auth1_1])
        self.assertEqual(len(self.short_note.comments), 2)

    def test_delete_tag_from_note(self):

        self.short_note.remove(tags=[self.tag_a])
        self.assertEqual(len(self.short_note.tags), 1)

    def test_delete_tag(self):

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

        note = Note.objects(slug="short-note").first()
        self.assertEqual(len(note.comments), 3)

        self.short_note.update(comments=[self.comment_auth2_2])

        note.reload()
        self.assertEqual(len(note.comments), 4)

    def test_add_tag_to_note(self):

        self.short_note.update(tags=[self.tag_c])
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]

        self.assertEqual(len(note_tags), 3)

        tag = Tag.objects(tag=self.tag_c.tag).first()
        self.assertEqual(tag.tag, self.tag_c.tag)

    def test_add_the_same_tag_multiple_times_to_note(self):

        self.short_note.update(tags=[self.tag_c])
        self.short_note.reload()
        self.short_note.update(tags=[self.tag_c])
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]

        self.assertEqual(len(note_tags), 3)

        tag = Tag.objects(tag=self.tag_c.tag).first()
        self.assertEqual(tag.tag, self.tag_c.tag)


    def test_add_notexisting_tag_to_note(self):

        new_tag = Tag(tag='d')

        self.short_note.update(tags=[new_tag])
        self.short_note.reload()
        note_tags = [tag.tag for tag in self.short_note.tags]

        self.assertEqual(len(note_tags), 3)

        tag = Tag.objects(tag=new_tag.tag).first()
        self.assertEqual(tag.tag, new_tag.tag)

    def test_edit_comment(self):
        pass

    def test_edit_note(self):
        pass

    def test_update_note_title(self):

        self.short_note.update(title="test")
        self.short_note.reload()
        self.assertEqual(self.short_note.title, 'test')

    def test_update_note(self):

        self.short_note.update(text="test")
        self.short_note.reload()
        self.assertEqual(self.short_note.text, 'test')

    def test_update_nonfield(self):

        self.short_note.update(doesnotexist="doesnotexist")
        self.short_note.reload()

