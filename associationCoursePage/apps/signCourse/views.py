# apps/signCourse/views.py
import os
import json
from django.shortcuts import render
from django.conf import settings
from .forms import SignupForm
from django.core.mail import send_mail
from uuid import uuid4
from django.template.loader import render_to_string

def sign(request, pk):
    file_url = settings.FILES_URL
    with open(f'{settings.BASE_DIR}{file_url}/information/courses.json', 'r', encoding='utf-8') as f:
        course_list = json.load(f)
        course = next((c for c in course_list if c['id'] == pk), None)

    if not course:
        return render(request, '404.html')

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data

            # Determine university and faculty based on choice
            university_choice = cleaned['university']
            price_val = float(course['price'])  # convert string to float or int

            if university_choice == 'kharazmi_engineering':
                university_name = "دانشگاه خوارزمی - دانشکده فنی و مهندسی"
                faculty_name = "دانشکده فنی و مهندسی"
                price = int(price_val * 0.5)  # 50% discount
            elif university_choice == 'kharazmi_other':
                university_name = "دانشگاه خوارزمی"
                faculty_name = cleaned.get('faculty_name', '')
                price = int(price_val)
            else:  # 'other'
                university_name = cleaned.get('university_name_other', '')
                faculty_name = cleaned.get('faculty_name', '')
                price = int(price_val)

            # Create folder for this person
            user_id = f"{cleaned['first_name']}_{cleaned['last_name']}_{uuid4().hex[:8]}"
            user_dir = os.path.join(settings.BASE_DIR, 'signups', user_id)
            os.makedirs(user_dir, exist_ok=True)

            # Save user data as JSON
            user_data = {
                'first_name': cleaned['first_name'],
                'last_name': cleaned['last_name'],
                'university': university_name,
                'faculty': faculty_name,
                'field': cleaned['field'],
                'telID': cleaned['telegramID'],
                'email': cleaned['email'],
                'referrer': cleaned['referrer'],
                'course_id': course['id'],
                'course_title': course['title'],
                'price': price,
            }
            with open(os.path.join(user_dir, 'details.json'), 'w', encoding='utf-8') as json_file:
                json.dump(user_data, json_file, ensure_ascii=False, indent=2)

            # Save receipt file
            receipt = cleaned['receipt']
            receipt_ext = os.path.splitext(receipt.name)[1]
            receipt_path = os.path.join(user_dir, f"receipt{receipt_ext}")
            with open(receipt_path, 'wb+') as destination:
                for chunk in receipt.chunks():
                    destination.write(chunk)


            message = render_to_string('emailreceipt.html', {'cleaned': cleaned})


            # send email of sign up to user
            send_mail( 'تأیید ثبت‌نام شما در دوره ' + course['title'],
                      "ثبت‌نام شما با موفقیت انجام شد.",
                      settings.EMAIL_HOST_USER, [cleaned['email']],
                      html_message=message)

            # Render success page
            return render(request, 'signsucc.html', {'name': cleaned['first_name'], 'files': file_url})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'course': course, 'files': file_url, 'form': form})
