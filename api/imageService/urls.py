from django.urls import path, include
from rest_framework.routers import DefaultRouter

from imageService.views import FileUploader

router = DefaultRouter()
router.register(r'v2', FileUploader)

urlpatterns = [
    path('', include(router.urls))
]
