from django.http import HttpResponse
from rest_framework import status


def is_superuser_view(request):
    if request.user.is_superuser:
        return HttpResponse(status=status.HTTP_200_OK)
    else:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
