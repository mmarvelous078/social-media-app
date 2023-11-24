import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ThreadsContent

# Signal for deleting Images 

@receiver(pre_delete, sender=ThreadsContent)
def delete_post_image(sender, instance, **kwargs):
    # Delete the image file when the associated Post instance is deleted
    if instance.content_img:

        image_path = os.path.join('images/', str(instance.content_img))
        if os.path.isfile(image_path):
            os.remove(image_path)