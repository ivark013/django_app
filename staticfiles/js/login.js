document.addEventListener("DOMContentLoaded", function () {
    // إخفاء رسالة الخطأ إذا كانت موجودة
    const errorElement = document.querySelector('.error');
    if (errorElement) {
        setTimeout(() => {
            errorElement.style.opacity = '0'; // استخدام تأثير تلاشي
            setTimeout(() => errorElement.style.display = 'none', 500); // إخفاء الرسالة نهائيًا
        }, 5000); // إخفاء الرسالة بعد 5 ثوانٍ
    }

    // إضافة تأثير على الحقول عند التفاعل
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = '#3498db';
            input.style.boxShadow = '0 0 8px rgba(52, 152, 219, 0.5)';
        });
        input.addEventListener('blur', () => {
            input.style.borderColor = '#ddd';
            input.style.boxShadow = 'none';
        });
    });
});
