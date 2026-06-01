from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router

from blog.api.pagination import DEFAULT_LIMIT, page_bounds
from blog.api.serializers import serialize_author, serialize_post_list, serialize_tag
from blog.models import Post, Tag, User
from blog.schemas import PostCreateIn, PostCreateOut, PostDetailOut, PostListOut

router = Router()


def _post_list_queryset():
    return Post.objects.select_related("author").prefetch_related("tags")


@router.get("/posts", response=list[PostListOut])
def list_posts(request, limit: int = DEFAULT_LIMIT, offset: int = 0):
    start, stop = page_bounds(limit, offset)
    posts = _post_list_queryset().filter(is_published=True).order_by("-created_at")[start:stop]
    return [serialize_post_list(post) for post in posts]


@router.get("/posts/search", response=list[PostListOut])
def search_posts(request, q: str, limit: int = DEFAULT_LIMIT, offset: int = 0):
    start, stop = page_bounds(limit, offset)
    posts = _post_list_queryset().filter(
        Q(title__icontains=q) | Q(body__icontains=q),
        is_published=True,
    ).order_by("-created_at")[start:stop]
    return [serialize_post_list(post) for post in posts]


@router.get("/posts/by-tag/{slug}", response=list[PostListOut])
def posts_by_tag(request, slug: str, limit: int = DEFAULT_LIMIT, offset: int = 0):
    tag = get_object_or_404(Tag, slug=slug)
    start, stop = page_bounds(limit, offset)
    posts = (
        tag.posts.select_related("author")
        .prefetch_related("tags")
        .filter(is_published=True)
        .order_by("-created_at")[start:stop]
    )
    return [serialize_post_list(post) for post in posts]


@router.get("/posts/{post_id}", response=PostDetailOut)
def get_post(request, post_id: int):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("tags"),
        id=post_id,
    )
    Post.objects.filter(id=post.id).update(view_count=F("view_count") + 1)
    post.view_count += 1
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author": serialize_author(post.author),
        "tags": [serialize_tag(tag) for tag in post.tags.all()],
        "comment_count": post.comments.count(),
        "view_count": post.view_count,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }


@router.post("/posts", response=PostCreateOut)
def create_post(request, payload: PostCreateIn):
    author = get_object_or_404(User, id=payload.author_id)
    post = Post.objects.create(
        author=author,
        title=payload.title,
        body=payload.body,
    )
    slugs = set(payload.tag_slugs)
    tags = list(Tag.objects.filter(slug__in=slugs))
    if len(tags) != len(slugs):
        found = {tag.slug for tag in tags}
        missing = ", ".join(sorted(slugs - found))
        raise Http404(f"Tags not found: {missing}")
    post.tags.set(tags)
    return {"id": post.id, "title": post.title}
