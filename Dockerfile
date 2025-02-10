# استخدام Python 3.9 كبيئة تشغيل
FROM python:3.12


# تعيين المجلد الرئيسي داخل الحاوية
WORKDIR /app

# تحديث الحزم وتثبيت المكتبات المطلوبة
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# نسخ ملفات المتطلبات وتثبيت حزم Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# نسخ باقي ملفات المشروع بعد تثبيت المتطلبات
COPY . .

# تعيين متغير البيئة للمنفذ
ENV PORT=8080

# تشغيل Gunicorn لتشغيل Django
CMD ["gunicorn", "servlliance.wsgi", "--bind", "0.0.0.0:8080"]
