# apps/signCourse/views.py
import os
import json
from django.shortcuts import render
from django.conf import settings
from .forms import SignupForm
from uuid import uuid4


def sign(request, pk):
    file_url = settings.FILES_URL
    with open(f'{settings.BASE_DIR}{file_url}/information/courses.json', 'r') as f:
        course_list = json.load(f)
        course = next((c for c in course_list if c['id'] == pk), None)

    if not course:
        return render(request, '404.html')

    # if someone sign up
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data

            # Create folder for this person in project BASE_DIR
            user_id = f"{cleaned['first_name']}_{cleaned['last_name']}_{uuid4().hex[:8]}"
            user_dir = os.path.join(settings.BASE_DIR, 'signups', user_id)
            os.makedirs(user_dir, exist_ok=True)

            # Save details as JSON
            user_data = {
                'first_name': cleaned['first_name'],
                'last_name': cleaned['last_name'],
                'university': cleaned['university'],
                'field': cleaned['field'],
                'phone': cleaned['phone'],
                'email': cleaned['email'],
                'referrer': cleaned['referrer'],
                'course_id': course['id'],
                'course_title': course['title'],
            }

            with open(os.path.join(user_dir, 'details.json'), 'w', encoding='utf-8') as json_file:
                json.dump(user_data, json_file, ensure_ascii=False, indent=2)

            # Save uploaded receipt file
            receipt = cleaned['receipt']
            receipt_ext = os.path.splitext(receipt.name)[1]
            receipt_path = os.path.join(user_dir, f"receipt{receipt_ext}")

            with open(receipt_path, 'wb+') as destination:
                for chunk in receipt.chunks():
                    destination.write(chunk)

            # Redirect or show success page
            return render(request, 'signsucc.html', {'name': cleaned['first_name'], 'files':file_url})
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'course': course, 'files': file_url, 'form': form})
