from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from ninja import NinjaAPI

from blog.api import router as blog_router

api = NinjaAPI()
api.add_router("/", blog_router)


def healthz(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz),
    path("api/", api.urls),
]
