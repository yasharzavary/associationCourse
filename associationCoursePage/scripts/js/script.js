// courses/static/courses/script.js

document.addEventListener('DOMContentLoaded', () => {
  const signupButtons = document.querySelectorAll('.signup-btn2');

  signupButtons.forEach(button => {
    button.addEventListener('click', event => {
      alert('لطفاً تا پایان فرآیند ثبت‌نام از ترک یا بارگذاری مجدد این صفحه خودداری فرمایید. با سپاس از همکاری شما.');
      // You could also add analytics or AJAX request here
    });
  });
});
