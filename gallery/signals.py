from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Image, Tag
from pathlib import Path
from django.core.files import File
import os
import subprocess

@receiver(post_save)
def rename_callback(sender, **kwargs):
    if not kwargs['created']: return
    instance = kwargs['instance']
    if sender == Image:
        file = Image.objects.get(id=instance.id)
        initial_path = file.file.path
        ext = "." + file.file.name.split('.')[-1]
        file.file.name = str(file.id) + ext
        new_path = settings.MEDIA_ROOT + "/" + file.file.name
        
        os.rename(initial_path, new_path)

        # for videos, generate a thumbnail
        if ext in (".mp4", ".webm"):
            file.is_video = True
            img_output_path = settings.MEDIA_ROOT + f"/thumbnails/{file.id}.jpg"
            subprocess.Popen(['ffmpeg', '-ss', '00:00:00.000', '-i', new_path, '-vframes', '1', '-vf', 'scale=350:-1', img_output_path])
        else:
            if ext in ('.gif', '.webp'):
                if subprocess.check_output(['identify', '-format', '%n', new_path]) != '1':
                    file.is_animated = True
            img_output_path = settings.MEDIA_ROOT + f"/thumbnails/{file.id}.jpg"
            subprocess.Popen(['convert', new_path + '[0]', '-resize', '350x', img_output_path])
        file.save()

        
        
        
        #raise NotImplementedError(file.file.name)
        #new_path = settings.MEDIA_ROOT

@receiver(pre_delete)
def delete_callback(sender, **kwargs):
    # when deleting the instance, delete the image as well.
    instance = kwargs['instance']
    if sender == Image:
        file = Image.objects.get(id=instance.id)
        path = file.file.path
        os.remove(path)

        thumb = settings.MEDIA_ROOT + f"/thumbnails/{file.id}.jpg"
        os.remove(thumb)
        

