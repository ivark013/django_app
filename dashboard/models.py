from django.db import models
from django.contrib.auth.models import User


class Camera(models.Model):
    """كاميرا مراقبة مرتبطة بالنظام"""

    camera_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.camera_id})"


class Alert(models.Model):
    """تنبيه يتعلق بالكاميرا"""

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="alerts")
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(
        max_length=50, choices=[("Low", "منخفض"), ("Medium", "متوسط"), ("High", "عالي")]
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"تنبيه من {self.camera.name} - {self.severity}"


class NotificationSettings(models.Model):
    """إعدادات التنبيهات للمستخدم"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    telegram_notifications = models.BooleanField(default=False)
    whatsapp_notifications = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"إعدادات التنبيهات للمستخدم {self.user.username}"
