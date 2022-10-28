import uuid
from django.db import models
from django.contrib.auth.models import User

# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, max_length=50, default="default")

    def retrieve(self):
        return {
            "id" : self.id,
            "public" : self.public,
            "user" : {
                "username" : self.user.username
            }
        }

# Create your models here.
class Image(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, unique=True)
    query = models.CharField(blank=False, max_length=50, default="default")
    
    def retrieve(self, request):
        return {
            "id" : self.id,
            "image_url" : request.build_absolute_uri('/').strip("/") + self.image_url.url,
            "query" : self.query,
            "file_id" : self.file.id
        }

    # def save(self, query = 'default', *args, **kwargs) :
    #     image_name = self.image_url.name.split('.')
    #     self.image_url.name = image_name[0] + f'-{query}.' + image_name[1]
    #     super(Image, self).save(*args, **kwargs)
