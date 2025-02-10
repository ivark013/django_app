# استخدام Python 3.9 كبيئة تشغيل
FROM python:3.9

# تعيين المجلد الرئيسي داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع إلى الحاوية
COPY . .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تعيين متغير البيئة للمنفذ
ENV PORT=8080

# تشغيل Gunicorn لتشغيل Django
CMD gunicorn servlliance.wsgi --bind 0.0.0.0:$PORT
