from django.contrib import admin
from django.urls import include, path

from mahsa.views import is_superuser_view

urlpatterns = [
    path('backend/nginx_auth_superuser/', is_superuser_view, name='nginx_superuser_auth'),
    path('backend/captcha/', include('captcha.urls')),
    path("backend/app/", include("app.urls")),
    path("backend/admin/", admin.site.urls),
]