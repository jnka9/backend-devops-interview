import json

import pytest
from django.test import Client

from blog.models import Comment, Post, User


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_create_comment(client):
    user = User.objects.create(
        username="bob", email="bob@example.com", display_name="Bob"
    )
    post = Post.objects.create(author=user, title="T", body="B")

    response = client.post(
        f"/api/posts/{post.id}/comments",
        data=json.dumps({"author_id": user.id, "body": "Nice post!"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert Comment.objects.filter(post=post, body="Nice post!").exists()


@pytest.mark.django_db
def test_list_comments(client):
    user = User.objects.create(
        username="bob", email="bob@example.com", display_name="Bob"
    )
    post = Post.objects.create(author=user, title="T", body="B")
    Comment.objects.create(post=post, author=user, body="Nice post!")

    response = client.get(f"/api/posts/{post.id}/comments")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["body"] == "Nice post!"
    assert data[0]["author"]["username"] == "bob"
