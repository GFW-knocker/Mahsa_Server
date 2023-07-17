from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('backend/captcha/', include('captcha.urls')),
    path("backend/app/", include("app.urls")),
    path("backend/admin/", admin.site.urls),
]