from dataclasses import field
from rest_framework import serializers
from imageService.models import Image, File


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__' 
        extra_kwargs = {
            'id': {'read_only': True}
        }


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__' 
        extra_kwargs = {
            'id': {'read_only': True}
        }
