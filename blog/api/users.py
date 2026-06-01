from django.shortcuts import get_object_or_404
from ninja import Router

from blog.api.serializers import serialize_user_detail
from blog.models import User
from blog.schemas import UserDetailOut

router = Router()


@router.get("/users/find", response=UserDetailOut)
def find_user_by_email(request, email: str):
    user = get_object_or_404(User, email=email)
    return serialize_user_detail(user)


@router.get("/users/{user_id}", response=UserDetailOut)
def get_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return serialize_user_detail(user)
