from django.urls import path, include

from . import views


app_name = "gallery"
urlpatterns = [
    path("", views.unfiltered, name="index"),
    path("untagged/", views.untagged, name="untagged"),
    path("<int:image_id>/", views.detail, name="detail"),
    path("upload/", views.upload, name="upload"),
    path("tags/", views.tags, name="tags"),
    path("ajax/add_tag", views.aj_add_tag, name="ajax add tag to image"),
    # path('', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='login')),
]
