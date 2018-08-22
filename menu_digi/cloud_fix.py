from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryResource, forms, uploader
from django.core.files.uploadedfile import UploadedFile


class CloudinaryFieldFix(CloudinaryField):
    def to_python(self, value):
        if isinstance(value, CloudinaryResource):
            return value
        elif isinstance(value, UploadedFile):
            return value
        elif value is None or value is False:
            return value
        else:
            return self.parse_cloudinary_resource(value)

class FixCloudinaryField(CloudinaryField):
    def to_python(self, value):
        if value is False:
            return value
        else:
            return super(FixCloudinaryField, self).to_python(value)
