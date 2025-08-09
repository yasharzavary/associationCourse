# apps/signCourse/forms.py
from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=100)
    last_name = forms.CharField(label="نام خانوادگی", max_length=100)

    UNIVERSITY_CHOICES = [
        ("kharazmi_engineering", "دانشگاه خوارزمی - دانشکده فنی و مهندسی"),
        ("kharazmi_other", "دانشگاه خوارزمی - سایر دانشکده‌ها"),
        ("other", "سایر دانشگاه‌ها"),
    ]
    university = forms.ChoiceField(label="دانشگاه", choices=UNIVERSITY_CHOICES)

    faculty_name = forms.CharField(
        label="نام دانشکده",
        max_length=100,
        required=False
    )

    university_name_other = forms.CharField(
        label="نام دانشگاه",
        max_length=100,
        required=False
    )

    field = forms.CharField(label="رشته تحصیلی", max_length=100)
    telegramID = forms.CharField(label="آیدی تلگرام", max_length=25)
    email = forms.EmailField(label="ایمیل")

    REFERRER_CHOICES = [
        ('channel_own', 'کانال رشته و دانشگاه خودم'),
        ('channel_association', 'کانال انجمن کامپیوتر خوارزمی'),
        ('friend', 'از طریق دوستان'),
        ('other', 'سایر'),
    ]
    referrer = forms.ChoiceField(label="نحوه آشنایی", choices=REFERRER_CHOICES, widget=forms.RadioSelect)
    receipt = forms.FileField(label="آپلود رسید پرداخت")

    def clean(self):
        cleaned = super().clean()
        uni_choice = cleaned.get("university")

        if uni_choice == "kharazmi_other" and not cleaned.get("faculty_name"):
            self.add_error("faculty_name", "لطفاً نام دانشکده را وارد کنید")

        if uni_choice == "other":
            if not cleaned.get("university_name_other"):
                self.add_error("university_name_other", "لطفاً نام دانشگاه را وارد کنید")
            if not cleaned.get("faculty_name"):
                self.add_error("faculty_name", "لطفاً نام دانشکده را وارد کنید")

        return cleaned
