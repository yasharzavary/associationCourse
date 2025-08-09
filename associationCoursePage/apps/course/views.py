from django.shortcuts import render
from django.conf import settings
import json

def course_detail(request, pk):
    file_url = settings.FILES_URL
    details = None
    # read details of course and teacher resumes for selected course.
    with open(f'{settings.BASE_DIR}{file_url}/information/courses.json', 'r') as f:
        for course in json.load(f):
            if course['id'] == pk:
                details = course
                break

    # if this course doesn't exist, return 404 error page.
    if not details:
        return render(request, '404.html')

    name = details['teacher'].split('.')[0]
    with open(f'{settings.BASE_DIR}{file_url}/information/teacher_resumes.json', 'r') as f:
        for teacher in json.load(f):
            if teacher['name'] == name:
                details.update(teacher)

    with open(f'{settings.BASE_DIR}{file_url}/information/session_details.json', 'r') as f:
        for detail in json.load(f):
            if detail['name'] == name:
                details.update(detail)


    return render(request, 'course_detail.html', {'course':details, 'files':file_url})
