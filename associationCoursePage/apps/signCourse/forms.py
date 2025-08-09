# apps/signCourse/forms.py
from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=100)
    last_name = forms.CharField(label="نام خانوادگی", max_length=100)
    university = forms.CharField(label="نام دانشگاه", max_length=100)
    field = forms.CharField(label="رشته تحصیلی", max_length=100)
    phone = forms.RegexField(label="شماره تلفن", regex=r'^09[0-9]{9}$')
    email = forms.EmailField(label="ایمیل")

    REFERRER_CHOICES = [
        ('channel_own', 'کانال رشته و دانشگاه خودم'),
        ('channel_association', 'کانال انجمن کامپیوتر خوارزمی'),
        ('friend', 'از طریق دوستان'),
        ('other', 'سایر'),
    ]
    referrer = forms.ChoiceField(label="نحوه آشنایی", choices=REFERRER_CHOICES, widget=forms.RadioSelect)
    receipt = forms.FileField(label="آپلود رسید پرداخت")
