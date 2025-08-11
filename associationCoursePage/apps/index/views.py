from django.shortcuts import render
from django.conf import settings
import json

def index(request):
    # read course details from course.json file.
    with open(f'{settings.BASE_DIR}{settings.FILES_URL}/information/courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)
    return render(request, 'index.html', {'courses': courses, 'files':settings.FILES_URL})

