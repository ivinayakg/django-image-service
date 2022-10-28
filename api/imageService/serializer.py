from dataclasses import field
from rest_framework import serializers
from .models import Image

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id', 'public'
        ]
