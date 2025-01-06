from typing import Any
from django.db.models import F
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse # not necessary once we do html for detail, results, vote
from django.urls import reverse
from django.views import generic
from .models import Image, Tag
from django.utils import timezone
from django.template import loader
from .forms import SearchForm, FileFieldForm, TagForm, ImageTagForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from .models import Image, Tag # tag unused... as of now.
from django.db.models import Count
from . import uploads
from .admin import ImageAdmin, TagAdmin
import gallery
# Create your views here.
IMAGES_PER_PAGE = 50 # obviously too low for now. but to demonstrate. change to 50 for normal.

# AJAX stuff
def aj_add_tag(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            tag = Tag.objects.get(name=request.POST["name"])
        except gallery.models.Tag.DoesNotExist:
            return JsonResponse({"status":"Error", "err_code":"not a valid tag"}, status=400)
        file = Image.objects.get(pk=request.POST['file'])
        
        if tag in file.tags.all():
            return JsonResponse({"status":"Error", "err_code":"duplicate"}, status=400)
        
        file.tags.add(tag)
    else:
        return JsonResponse({"status":"error", "err_code":"No permissions or incorrect request type"})
    return JsonResponse({"status":"OK", "color": tag.color})

def aj_remove_tag(request):
    if request.method == "POST" and request.user.is_authenticated and request.user.has_perm('gallery.delete_tag'):
        image = Image.objects.get(pk=request.POST['file'])
        try:
            tag = Tag.objects.get(name=request.POST['name'])
        except gallery.models.Tag.DoesNotExist:
            return JsonResponse({"status":"Error", "err_code":"not a valid tag"}, status=400)
        if tag in image.tags.all():
            image.tags.remove(tag)
        return JsonResponse({"status":"OK"})
    return JsonResponse({"status":"Error", "err_code":"No permissions"})
    
def aj_view_image(request):
    # not sending or retrieving data...
    # not entirely sure how ajax works...
    # but send the tags, and the full res image, and upvotes
    if request.method == "GET":
        file = Image.objects.get(pk=request.GET['id'])
        tags = []
        for tag in file.tags.all():
            tag_json = {
                'name': tag.name,
                'color': tag.color
            }
            tags.append(tag_json)
        response = {
            'tags': tags,
            'votes': file.votes,
            'date': file.pub_date,
            'is_video': file.is_video,
            'file_name': file.file.name,
        }
        return JsonResponse(response, safe=False)
    else:
        raise ValueError
    
def aj_get_matching_tags(request):
    if request.method == "GET":
        query = request.GET['text']
        # nope! i need to manually serialize it.
        tags = []
        for tag in Tag.objects.filter(name__icontains=query).annotate(Count("image")).order_by("-image__count"):
            tags.append({
                'name': tag.name,
                'color': tag.color,
                'tag_count': tag.images.count(),
            })
            if len(tags) > 5: break # so you won't get a billion in some edge case

        return JsonResponse({'tags':tags})
    else:
        raise ValueError

def detail(request, image_id):
    file = Image.objects.get(id=image_id)
    template = loader.get_template("gallery/image.html")
    context = {
        "file": file,
        "red": file.tags.filter(color="R"),
        "green": file.tags.filter(color="G"),
        "purple": file.tags.filter(color="P"),
        "none": file.tags.filter(color="N"),
    }
    if request.method == "POST":
        form = ImageTagForm(request.POST)
        try:
            tag = Tag.objects.get(name=request.POST["name"])
        except ValueError:
            return HttpResponse(template.render(context, request))
        if form.is_valid():
            if not file.tags.contains(tag):
                file.tags.add(tag)
            return HttpResponseRedirect(f"/gallery/{image_id}/")
        else:
            raise ValueError("Invalid... for some reason.")

    return HttpResponse(template.render(context, request))

def unfiltered(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        tags = []
        if (form.data.get('tag_list' , '').strip() != ''):
            tags = form.data['tag_list'].split(",")

            if tags[-1] in ('', ' '): tags.pop()

            images = Image.objects.all()
            for i in range(len(tags)):
                # removing leading/trailing whitespace
                tags[i] = tags[i].strip()
                
                # filtering out unwanted images
                images = images.filter(tags__name=tags[i])
                # terminating early if images becomes null
                if not len(images):
                    break
        
            image_list = images.order_by("-pub_date") # this should be changeable in the future
        else:
            image_list = Image.objects.order_by("-pub_date")
    template = loader.get_template("gallery/index.html")

    paginator = Paginator(image_list, IMAGES_PER_PAGE) 
    page_number = 1 if request.GET.get("page") is None else request.GET.get("page")
    page_images = paginator.page(page_number)

    tag_rank = Ranking()
    for image in page_images:
        tag_rank.update(image.tags.all())
    
    # getting selected tags
    selected_tags = []
    print(tags)
    for tag in tags:
        selected_tags.append(Tag.objects.get(name=tag))

    context = {
        "page_images": page_images,
        "image_tags": tag_rank.get_highest_n(15)[::-1],
        "selected_tags": selected_tags,
    }
    return HttpResponse(template.render(context, request))

# i'm leaving both the class and functions to see if they work?
def upload(request):
    context = {}
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            context["errors"] = uploads.handle_uploaded_file(request.FILES)
            return HttpResponseRedirect("/upload/")
        else:
            raise ValueError("Invalid... for some reason.")
    else:
        form = FileFieldForm()
    context["form"] = form
    return render(request, "gallery/upload.html", context)

def tags(request):
    if request.method == "GET":
        # search for tags
        form = SearchForm(request.GET)
        query = form.data.get('tag_search', '')
        if query != "":
            tag_list = Tag.objects.filter(name__icontains=query).annotate(Count("image")).order_by("-image__count")
        else:
            tag_list = Tag.objects.annotate(Count("image")).order_by("-image__count")
    elif request.method == "POST":
        # create one or more tags
        tag_list = Tag.objects.annotate(Count("image")).order_by("-image__count")
        form = TagForm(request.POST)
        if form.is_valid():
            Tag(name=form.cleaned_data["name"], color=form.cleaned_data["category"]).save()
            return HttpResponseRedirect("/tags/")

        else:
            raise ValueError(request.POST)

        raise NotImplementedError("do it first, ya dingus.")
    paginator = Paginator(tag_list, IMAGES_PER_PAGE) 
    page_number = 1 if request.GET.get("page") is None else request.GET.get("page")
    page_tags = paginator.page(page_number)

    template = loader.get_template("gallery/tags.html")
    context = {
        "tags": page_tags
    }
    return HttpResponse(template.render(context, request))




def untagged(request):
    image_list = Image.objects.annotate(tag_count=Count("tags")).filter(tag_count=0)
    image_list = Image.objects.order_by("-pub_date")
    template = loader.get_template("gallery/index.html")

    paginator = Paginator(image_list, IMAGES_PER_PAGE)
    page_number = 1 if request.GET.get("page") is None else request.GET.get("page")
    page_images = paginator.page(page_number)
    context = {
        "page_images": page_images,
    }
    return HttpResponse(template.render(context, request))


# this is just so that i can not have a bajillion tags while having the ones be there not be random.
class Ranking:
    # okay so have it be like this:
    # initialize it as blank
    # 
    scores: list[int] # scores, for points...
    ids: list[Any] # the ids, for scoring
    def __init__(self):
        self.scores = []
        self.ids = []
    
    def update(self, iterable):
        for item in iterable:
            if item not in self.ids:
                self.ids.insert(0, item)
                self.scores.insert(0, 1)
            else:
                index = self.ids.index(item)
                self.scores[index] += 1
                while index + 1 < len(self.ids) and self.scores[index] > self.scores[index + 1]:
                    self._swap(index)
                    index += 1

    def _swap(self, index):
        score = self.scores[index]
        i = self.ids[index]
        self.scores[index] = self.scores[index + 1]
        self.ids[index] = self.ids[index + 1]
        self.scores[index + 1] = score
        self.ids[index + 1] = i

    def get_highest_n(self, num: int):
        # please don't make it negative
        # get the top n ids (don't care about scores)
        return self.ids[-num:]