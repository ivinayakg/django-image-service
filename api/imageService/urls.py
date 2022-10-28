from django.urls import path
from .views import getFiles, getImage, uploadImage2, uploadImage_view

urlpatterns = [
    path('create/', uploadImage2),
    path('<str:pk>/view/', getImage),
    path('all/', getFiles),
]
