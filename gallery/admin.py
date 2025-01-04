from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import Tag, Image
# Register your models here.

class AdminMediaWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            if value.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
                output.append(f'<img src="{value.url}" width="300" height="auto" />')
            elif value.url.endswith(('mp4', 'webm', 'ogg')):
                output.append(f'<video width="300" height="auto" controls>'
                              f'<source src="{value.url}" type="video/mp4">'
                              f'Your browser does not support the video tag.</video>')
        #output.append(super().render(name, value, attrs, renderer))
        return mark_safe(''.join(output))
        

class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

    file = forms.FileField(widget=AdminMediaWidget)

    def __init__(self, *args, **kwargs):
        super(ImageAdminForm, self).__init__(*args, **kwargs)
        self.fields['file'].disabled = True  # Disable changing the image file
        self.fields['votes'].disabled = True  # Disable changing the votes


class ImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ('file_link', 'thumbnail_preview')

    def file_link(self, obj):
        return mark_safe(f'<a href="/admin/gallery/image/{obj.id}/change/">{obj.id}</a>')
    file_link.short_description = 'Edit Tags'

    def thumbnail_preview(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.thumbnail_url()}" width="50" height="50" />') 
        return "No Image"
    thumbnail_preview.short_description = 'Thumbnail Preview'

class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(Tag)
