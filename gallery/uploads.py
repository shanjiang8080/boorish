from django.conf import settings
from .models import Image

def handle_uploaded_file(f) -> list[str]:
    # this is assuming it's one file and not several...
    # returns errors, if they exist.
    errors = []

    for file in f.getlist('uh'):
        if validate_file_type(file): # maybe do a more robust error things.... or whatever who cares idk.
            print(file.name)
            ext = file.name.split(".")[-1]
            with open(f"{settings.MEDIA_ROOT}/file.{ext}", "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            Image(file=file).save()
        else:
            errors.append(f"File {file.name} has the wrong file type.")
    return errors

def validate_file_type(f):
    ext = f.name.split('.')[-1].lower()
    if ext not in (
        'png', 
        'avif',
        'jpg',
        'jpeg',
        'jfif',
        'pjpeg',
        'pjp',
        'gif',
        'webp',
        'apng',
        'svg',
        # videos
        'mp4',
        'webm',
    ):
        return False
    return True
