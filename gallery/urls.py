from django.urls import path, include

from . import views


app_name = "gallery"
# I cut out this: path("<int:image_id>", views.detail, name="detail"),
urlpatterns = [
    path("", views.unfiltered, name="index"),
    path("untagged/", views.untagged, name="untagged"),
    path("upload/", views.upload, name="upload"),
    path("tags/", views.tags, name="tags"),
    path("a/add_tag", views.aj_add_tag, name="ajax add tag to image"),
    path("a/view_image", views.aj_view_image, name="ajax view image"),
    path("a/search_tag", views.aj_get_matching_tags, name="ajax get tags"),
    # path('', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='login')),
]
