from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

# this should be unused because it should be a thing instead...
def update_filename(instance, filename):
    num = str(instance.file)
    ext = "." + filename.split('.')[-1]
    return num + ext

def validate_no_comma(tag: str):
    if ',' in tag:
        raise ValidationError("Tags cannot have commas.", params={"tag": tag})

def validate_no_leading_trailing_spaces(tag: str):
    if tag.strip() != tag:
        raise ValidationError("Tags cannot start or end with a space.", params={"tag": tag})

class Tag(models.Model):
    R = "R"
    G = "G"
    P = "P"
    N = "N"
    TAG_COLORS = {
        R:"Artist",
        G:"Character",
        P:"Copyright",
        N:"Description",
    }
    name = models.CharField(unique=True, max_length=255, validators=[validate_no_comma, validate_no_leading_trailing_spaces]) # there cannot possibly be use for more characters
    color = models.CharField(max_length=1, choices=TAG_COLORS, default=N) # color of the tag
    def __str__(self):
        return f"{self.name} ({self.color})"
    # i want to have a self.is_dangling() function but i don't know how when it's on the other model...

class Image(models.Model):
    file = models.FileField(
                            max_length=255,
                            validators=[FileExtensionValidator(allowed_extensions=[
                                # images
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
                                ])]
                            ) # not just an image field, should accept videos as well.
    is_video = models.BooleanField(default=False, editable=False)
    is_animated = models.BooleanField(default=False, editable=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    votes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="images", related_query_name="image", blank=True)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.file.name # not very helpful but waddya gonna do
    
    def thumbnail_url(self):
        return f"/media/thumbnails/{self.id}.jpg"
