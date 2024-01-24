from django.shortcuts import render
from django.http import JsonResponse
from .models import Image

def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = Image(img=request.FILES['image'])
        image.save()

        return JsonResponse({'result_image': image.rmbg_img.url})

    return JsonResponse({'error': 'Invalid request'})
