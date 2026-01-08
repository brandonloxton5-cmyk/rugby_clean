from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bulletin/", include("bulletin.urls")),
    path("", include("api.urls")),
]
