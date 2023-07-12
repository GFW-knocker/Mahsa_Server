from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("backend/app/", include("app.urls")),
    path("backend/admin/", admin.site.urls),
]