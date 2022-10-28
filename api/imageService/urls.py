from django.urls import path
from .views import getFiles, getImage, uploadImage
urlpatterns = [
    path('create/', uploadImage),
    path('<str:pk>/view/', getImage),
    path('all/', getFiles),
]
