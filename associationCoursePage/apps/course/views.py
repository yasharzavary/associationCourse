from django.shortcuts import render
from django.conf import settings
import json

def course_detail(request, pk):
    file_url = settings.FILES_URL
    details = None
    
    # FIX: Added encoding='utf-8' to correctly read Persian characters
    with open(f'{settings.BASE_DIR}{file_url}/information/courses.json', 'r', encoding='utf-8') as f:
        for course in json.load(f):
            if course['id'] == pk:
                details = course
                break

    # if this course doesn't exist, return 404 error page.
    if not details:
        return render(request, '404.html')

    name = details['teacher'].split('.')[0]
    
    # FIX: Added encoding='utf-8'
    with open(f'{settings.BASE_DIR}{file_url}/information/teacher_resumes.json', 'r', encoding='utf-8') as f:
        for teacher in json.load(f):
            if teacher['name'] == name:
                details.update(teacher)

    # FIX: Added encoding='utf-8'
    with open(f'{settings.BASE_DIR}{file_url}/information/session_details.json', 'r', encoding='utf-8') as f:
        for detail in json.load(f):
            if detail['name'] == name:
                details.update(detail)


    return render(request, 'course_detail.html', {'course':details, 'files':file_url})