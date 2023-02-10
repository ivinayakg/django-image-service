import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File as FileOpen
import os
from random import random

from imageService.services import query_decrypt, query_image_generator


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, max_length=50,
                            default="default")

    def retrieve(self):
        return {
            "id": self.id,
            "public": self.public,
            "user": {
                "username": self.user.username
            }
        }


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, unique=True)
    query = models.CharField(blank=False, max_length=50, default="default")

    def retrieve(self, request):
        return {
            "id": self.id,
            "image_url": request.build_absolute_uri('/').strip("/") + self.image_url.url,
            "query": self.query,
            "file_id": self.file.id
        }

    @classmethod
    def get_image(self, file, query):
        image = None
        try:
            image = self.objects.get(file=file, query=query)
        except ObjectDoesNotExist as Error:
            image = self.objects.get(file=file, query="default")
            try:
                if 'Image matching query does not exist.' in Error.args:
                    new_image = Image(file=file, query=query)
                    (new_image_file, new_image_name) = query_image_generator(
                        image=image.image_url.path, query=query_decrypt(query), image_name=new_image.id.hex)
                    new_image.image_url.save(
                        new_image_name, FileOpen(open(new_image_file, 'rb')))
                    if os.path.exists(new_image_file):
                        os.remove(new_image_file)
                    new_image.save()
                    image = new_image
            except Exception as e:
                pass
        finally:
            return image
