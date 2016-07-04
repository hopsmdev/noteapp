import json
from django.test import RequestFactory
from notes.tests.utils import TestCaseMongo, TestDataFactory
from notes.api.views import *


class NoteGETApiTest(TestCaseMongo, TestDataFactory):

    def setUp(self):
        self.data_setup()
        self.factory = RequestFactory()

    def test_get_notes(self):

        request = self.factory.get('/api/v1/notes/')
        response = NoteList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_note_detail_id(self):

        _id = str(self.short_note.id)
        request = self.factory.get('/api/v1/notes/{}'.format(_id))

        view = NoteDetail.as_view()
        response = view(request, id=_id)
        self.assertEqual(response.status_code, 200)

    def test_get_note_detail_slug(self):

        slug = self.short_note.slug
        request = self.factory.get('/api/v1/notes/{}'.format(str(slug)))

        view = NoteDetailSlug.as_view()
        response = view(request, slug=slug)
        self.assertEqual(response.status_code, 200)


class NotePOSTApiTest(TestCaseMongo, TestDataFactory):

    def setUp(self):
        self.data_setup()
        self.factory = RequestFactory()

    def test_post_note(self):

        data = {
            'title': 'Test POST',
            'text': 'post text',
            'tags': [{'tag': 'a'}, {'tag': 'b'}],
            'comments': []
        }

        print(json.dumps(data))
        request = self.factory.post(
            '/api/v1/notes/', json.dumps(data), content_type="application/json")
        response = NoteList.as_view()(request)
        print(response.data)
        self.assertEqual(response.status_code, 201)


class TagGETApiTest(TestCaseMongo, TestDataFactory):

    def setUp(self):
        self.data_setup()
        self.factory = RequestFactory()


    def test_get_tags(self):

        request = self.factory.get('/api/v1/tags/')
        response = TagList.as_view()(request)
        self.assertEqual(response.status_code, 200)






