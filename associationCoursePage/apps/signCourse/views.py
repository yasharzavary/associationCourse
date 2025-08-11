# apps/signCourse/views.py
import os
import json
from django.shortcuts import render, HttpResponse
from django.conf import settings
from .forms import SignupForm
from django.core.mail import send_mail
from uuid import uuid4
from django.template.loader import render_to_string
from string import ascii_lowercase, digits
from random import choice


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

            track_code = ''.join([choice(digits + ascii_lowercase) for _ in range(10)])
            have = True
            while have:
                have = False
                with open(f'{settings.BASE_DIR}{file_url}/core/track_codes.txt', 'r', encoding='utf-8') as f:
                    line_read_file = {line.strip() for line in f}
                    if track_code in line_read_file:
                        ''.join([choice(digits + ascii_lowercase) for _ in range(10)])
                        have = True

            with open(f'{settings.BASE_DIR}{file_url}/core/track_codes.txt', 'a', encoding='utf-8') as f:
                f.write(track_code + '\n')

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
                'track_code': track_code,
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

            message = render_to_string('emailreceipt.html', {'cleaned': cleaned,
                                                             'track_code': track_code})

            try:
                # send email of sign up to user
                send_mail('تأیید ثبت‌نام شما در دوره ' + course['title'],
                          "ثبت‌نام شما با موفقیت انجام شد.",
                          settings.EMAIL_HOST_USER, [cleaned['email']],
                          html_message=message)
                # Render success page
                return render(request, 'signsucc.html', {'name': cleaned['first_name'],
                                                         'files': file_url, 'track_code': track_code})
            except:
                del cleaned['receipt']
                os.mkdir(f'{settings.BASE_DIR}{file_url}/core/emails/{track_code}')
                with open(f'{settings.BASE_DIR}{file_url}/core/emails/{track_code}/details.json', 'w', encoding='utf-8') as f:
                    json.dump({'cleaned': cleaned, 'track_code': track_code, 'course': course},
                              f, ensure_ascii=False, indent=2)

                # Render success page
                return render(request, 'signsucc.html', {'name': cleaned['first_name'],
                                                         'files': file_url, 'track_code': track_code,
                                                         'error': 'در حال حاضر سرور ایمیل در دسترس نیست، بعد از اتصال تاییدیه ثبت نام شما ارسال خواهد شد.'})
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'course': course, 'files': file_url, 'form': form})


def send_emails_offline(req):
    base_url = settings.BASE_DIR
    file_url = settings.FILES_URL
    for file_dir in os.listdir(f'{base_url}{file_url}core/emails'):
        with open(f'{base_url}{file_url}core/emails/{file_dir}/details.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        cleaned = data['cleaned']
        course = data['course']
        track_code = data['track_code']

        message = render_to_string('emailreceipt.html', {'cleaned': cleaned,
                                                         'track_code': track_code})
        try:
            # send email of sign up to user
            send_mail('تأیید ثبت‌نام شما در دوره ' + course['title'],
                      "ثبت‌نام شما با موفقیت انجام شد.",
                      settings.EMAIL_HOST_USER, [cleaned['email']],
                      html_message=message)
            for file in os.listdir(f'{base_url}{file_url}core/emails/{file_dir}'):
                os.remove(os.path.join(f'{base_url}{file_url}core/emails/{file_dir}', file))
            os.rmdir(f'{base_url}{file_url}core/emails/{file_dir}')
        except Exception as e:
            print(e)
            print(f'{file_dir} doesn\'t send to user')

    return HttpResponse('<h1>done</h1>')
