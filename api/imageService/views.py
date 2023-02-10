from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from django.db.models import Q as query_filter_utility

from imageService.models import File, Image
from imageService.serializer import ImageSerializer, FileSerializer


class FileUploader(CreateModelMixin, ReadOnlyModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'id'
    # authentication_classes =

    def get_file_data(self, request):
        return {
            "public": request.data.get('public', False),
            "user": request.user.id
        }

    def get_image_data(self, request, file):
        image_file = request.data.get('image')
        if not image_file:
            raise Exception("Please provide an image in the form.")
        if not file:
            raise Exception("Something went wrong.")
        return {
            "image_url": image_file,
            "file": file
        }

    def get_queryset(self):
        user = self.request.user
        get_public = self.request.query_params.get('public', False)
        if user and get_public:
            return self.queryset.filter(query_filter_utility(public=get_public) | query_filter_utility(user=user.id))
        elif user and not get_public:
            return self.queryset.filter(user=user.id)
        else:
            return self.queryset.filter(public=True)

    def create(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=self.get_file_data(request))
        file_serializer.is_valid(raise_exception=True)
        file_object = file_serializer.create(
            validated_data=file_serializer.validated_data)
        try:
            image_serilizer = ImageSerializer(
                data=self.get_image_data(request, file=file_object.id))
            image_serilizer.is_valid()
            image_object = image_serilizer.create(
                validated_data=image_serilizer.validated_data)
        except Exception as exception:
            file_object.delete()
            raise exception
        headers = self.get_success_headers(file_serializer.data)
        return Response({"image": image_object.retrieve(request), "file": file_object.retrieve()}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"message": "Successfully done", "data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        file_instance = self.get_object()
        image_query = request.query_params.get("query", "default")
        image = Image.get_image(file=file_instance, query=image_query)
        return Response({"message": "Successfully done", "data": image.retrieve(request)})
