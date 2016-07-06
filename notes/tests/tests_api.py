import json
from django.test import RequestFactory
from notes.tests.utils import TestCaseMongo, TestDataFactory
from notes.api.views import *


class ApiTest(TestCaseMongo, TestDataFactory):

    def setUp(self):
        self.data_setup()
        self.factory = RequestFactory()


class NoteGETApiTest(ApiTest):

    def test_get_notes(self):

        request = self.factory.get('/api/v1/notes/')
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_note_detail_id(self):

        _id = str(self.short_note.id)
        request = self.factory.get('/api/v1/notes/{}'.format(_id))

        response = NoteDetail.as_view()(request, id=_id)
        self.assertEqual(response.status_code, 200)

    def test_get_note_detail_notexistid(self):

        request = self.factory.get('/api/v1/notes/123')
        response = NoteDetail.as_view()(request, id='123')
        self.assertEqual(response.status_code, 404)

    def test_get_note_detail_slug(self):

        slug = self.short_note.slug
        request = self.factory.get('/api/v1/notes/{}'.format(str(slug)))

        response = NoteDetailSlug.as_view()(request, slug=slug)
        self.assertEqual(response.status_code, 200)


class NotePOSTApiTest(ApiTest):

    def test_post_note(self):

        data = {
            'title': 'Test POST',
            'text': 'post text',
            'tags': [{'tag': 'a'}, {'tag': 'b'}],
            'comments': [
                {
                    "author": "Author1",
                    "email": "author1@test.com",
                    "text": "First comment of Author1"
                },
                {
                    "author": "Author1",
                    "email": "author1@test.com",
                    "text": "Second comment of Author1"
                }]
        }

        request = self.factory.post(
            '/api/v1/notes/', json.dumps(data), content_type="application/json")
        response = NoteList.as_view()(request)

        self.assertTrue(response.data['comments'])
        self.assertTrue(response.data['tags'])
        self.assertEqual(response.status_code, 201)

        note_id = response.data['id']

        request = self.factory.get('/api/v1/notes/{}'.format(note_id))
        response = NoteDetail.as_view()(request, id=note_id)
        self.assertEqual(response.status_code, 200)


class NotePUTApiTest(ApiTest):

    def test_put_note(self):

        data = {
            'title': 'Test POST',
            'text': 'post text',
            'tags': [{'tag': 'e'}, {'tag': 'f'}],
            'comments': [
                {
                    "author": "Author3",
                    "email": "author3@test.com",
                    "text": "First comment of Author3"
                },
                {
                    "author": "Author3",
                    "email": "author3@test.com",
                    "text": "Second comment of Author3"
                }]
        }

        note_id = self.short_note.id
        url = '/api/v1/notes/{}'.format(str(note_id))

        request = self.factory.put(
            url, json.dumps(data), content_type="application/json")
        response = NoteDetail.as_view()(request, id=note_id)

        self.assertTrue(response.data['comments'])
        self.assertTrue(response.data['tags'])
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('/api/v1/notes/{}'.format(note_id))
        response = NoteDetail.as_view()(request, id=note_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tags']), 4)
        self.assertEqual(len(response.data['comments']), 5)


class NoteDELETEApiTest(ApiTest):

    def test_delete_note(self):

        note_id = self.short_note.id
        url = '/api/v1/notes/{}'.format(str(note_id))

        # Confirm that note exists
        request = self.factory.get(url)
        response = NoteDetail.as_view()(request, id=note_id)
        self.assertEqual(response.status_code, 200)

        # Removing note
        request = self.factory.delete(url)
        response = NoteDetail.as_view()(request, id=note_id)

        # Confirm that note was removed
        request = self.factory.get(url)
        response = NoteDetail.as_view()(request, id=note_id)
        self.assertEqual(response.status_code, 404)


################################################################################
#                                  TAGS
################################################################################

class TagGETApiTest(ApiTest):

    def test_get_tags(self):

        request = self.factory.get('/api/v1/tags/')
        response = TagList.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TagPOSTApiTest(ApiTest):

    def test_post_tag(self):

        data = {
            'tag': 'XXX'
        }

        request = self.factory.post(
            '/api/v1/tags/', json.dumps(data), content_type="application/json")
        response = TagList.as_view()(request)
        self.assertEqual(response.status_code, 201)

        request = self.factory.get('/api/v1/tags/')
        response = TagList.as_view()(request)
        self.assertEqual(len(response.data), 4)


class TagDELETEApiTest(ApiTest):

    def test_delete_tag(self):
        request = self.factory.delete('/api/v1/tags/a')
        response = TagDetail.as_view()(request, tag='a')
        self.assertEqual(response.status_code, 204)

        request = self.factory.get('/api/v1/tags/')
        response = TagList.as_view()(request)
        self.assertEqual(len(response.data), 2)

        # Confirm that tag from note was also removed
        _id = str(self.short_note.id)
        request = self.factory.get('/api/v1/notes/{}'.format(_id))
        response = NoteDetail.as_view()(request, id=_id)
        self.assertEqual(len(response.data['tags']), 1)
