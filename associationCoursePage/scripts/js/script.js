// courses/static/courses/script.js

document.addEventListener('DOMContentLoaded', () => {
  const signupButtons = document.querySelectorAll('.signup-btn');

  signupButtons.forEach(button => {
    button.addEventListener('click', event => {
      alert('در حال انتقال به فرم ثبت‌نام دوره...');
      // You could also add analytics or AJAX request here
    });
  });
});
