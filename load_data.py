from notes.models import *
from mongoengine.connection import connect, disconnect, register_connection

MONGODB_NAME = "testdb"

MONGO_DATABASE_OPTIONS = {
    "host": '127.0.0.1',
    "port": 27017,
    "username": 'test',
    "password": 'test',
}

register_connection('default', MONGODB_NAME, **MONGO_DATABASE_OPTIONS)

disconnect()
connect('testdb')

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


comment_auth1_1 = Comment(**comment_1)
comment_auth1_2 = Comment(**comment_2)
comment_auth2_1 = Comment(**comment_3)
comment_auth2_2 = Comment(**comment_4)

tag_a = Tag(tag='a')
tag_b = Tag(tag='b')
tag_c = Tag(tag='c')

tag_a.save()
tag_b.save()
tag_c.save()

short_note = Note(
    title="test note",
    text="test note text",
    tags=[tag_a, tag_b],
    slug="short-note",
    is_published=True,
    comments=[
        comment_auth1_1,
        comment_auth1_2,
        comment_auth2_1])

long_note = Note(
    title="test long note",
    text="".join(str(i) for i in range(0, 100)),
    tags=[tag_a, tag_b, tag_c],
    is_published=True,
    comments=[
        comment_auth1_1,
        comment_auth1_2,
        comment_auth2_1])

note_noslug = Note(
    title="test noslug note",
    text="test noslug note text",
    tags=[tag_a, tag_b],)


short_note.save()
long_note.save()
note_noslug.save()