from django.shortcuts import get_object_or_404
from ninja import Router

from blog.api.pagination import DEFAULT_LIMIT, page_bounds
from blog.api.serializers import serialize_comment
from blog.models import Comment, Post, User
from blog.schemas import CommentCreateIn, CommentCreateOut, CommentOut

router = Router()


@router.get("/posts/{post_id}/comments", response=list[CommentOut])
def list_comments(request, post_id: int, limit: int = DEFAULT_LIMIT, offset: int = 0):
    get_object_or_404(Post.objects.only("id"), id=post_id)
    start, stop = page_bounds(limit, offset)
    comments = (
        Comment.objects.select_related("author")
        .filter(post_id=post_id)
        .order_by("created_at")[start:stop]
    )
    return [serialize_comment(comment) for comment in comments]


@router.post("/posts/{post_id}/comments", response=CommentCreateOut)
def create_comment(request, post_id: int, payload: CommentCreateIn):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, id=payload.author_id)
    comment = Comment.objects.create(post=post, author=author, body=payload.body)
    return {"id": comment.id}
