from django.shortcuts import render, redirect
from uploader.forms import ImageFileForm
from uploader.models import ImageFile


def home(request):
    data = dict()

    image_form = ImageFileForm(request.POST or None, request.FILES or None)
    if image_form.is_valid():
        image_form.save()
        image_form = ImageFileForm()
        redirect('home')

    image_list = ImageFile.objects.all()

    data['image_form'] = image_form
    data['image_list'] = image_list
    return render(request, "uploader/index.html", data)
