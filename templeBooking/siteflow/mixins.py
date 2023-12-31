import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models

class ResizeImageMixin:
    def resize(self, imageField: models.ImageField, size:tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert('RGB')
        source_image.thumbnail(size)  # Resize to size
        output = BytesIO()
        source_image.save(output, format='JPEG') # Save resize image to bytes
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.jpeg'
        imageField.save(random_name, file, save=False)


class customerloginmixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_vendor==True:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)