from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File as FileOpen
import os

from .models import File, Image
from .services import query_decrypt,query_image_generator

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def uploadImage(request, *args, **kwargs):
    image_file = request.data.get('image')
    image_file_name = image_file.name.split('.')
    try:
        public = True
        file = File(user = request.user, public=public)
        image = Image(image_url = image_file, file = file)

        image.image_url.name = image_file_name[0] + '-default.' + image_file_name[1]
        file.name = image_file_name[0]
        file.save()
        image.save()

        return Response({"message" : "Successfully done", "data" : {"image" : image.retrieve(request), "file" : file.retrieve()}})
    except Exception as Error:
        print(Error)
        return Response({"message" : "Something Went Wrong!"})

@api_view(['GET'])
def getFiles(request, *args, **kwargs):
    files = File.objects.all()
    result = []
    for x in files:
        result.append(x.pk)
    return Response({"message" : "Successfully done", "data" : result})

@api_view(["GET"])
def getImage(request, pk, *args, **kwargs):
    file = File.objects.get(pk=pk)
    image = Image.objects.get(file=file, query="default")
    image_query = request.query_params.get('query')
    try:
        if image_query:
            image = Image.objects.get(file=file, query=image_query)
    except ObjectDoesNotExist as Error:
        if 'Image matching query does not exist.' in Error.args:
            (new_image_path, new_image_extension) = query_image_generator(image=image.image_url.path, query=query_decrypt(image_query), query_str=image_query)
            new_image = Image(file=file, query=image_query)
            new_image.image_url.save(file.name + "-" + image_query + "." + new_image_extension, FileOpen(open(new_image_path, 'rb')))
            if os.path.exists(new_image_path):
                os.remove(new_image_path)
            new_image.save()
            image = new_image
    finally:
        return Response({"message" : "Successfully done", "data" : image.retrieve(request)})
