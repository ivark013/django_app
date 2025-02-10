import cv2
import numpy as np
from .models import Alert
import logging
import torch
import requests
from django.core.mail import send_mail
from django.conf import settings
import os
from ultralytics import YOLO

logger = logging.getLogger(__name__)

YOLO_MODEL = None


def load_yolo_model(model_name):
    global YOLO_MODEL
    print(f"Loading YOLO model: {model_name}")
    model_path = settings.AI_MODELS.get(model_name, {}).get("model")
    if not model_path or not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    YOLO_MODEL = YOLO(model_path)
    YOLO_MODEL.eval()
    return YOLO_MODEL


def preprocess_image(image):
    """
    Preprocess the image for YOLO model input.
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))  # Change to 640x640 to match YOLO v5 input size
    img = img.transpose((2, 0, 1))
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img


def detect_objects(image, model_name, camera):
    global YOLO_MODEL
    if YOLO_MODEL is None:
        YOLO_MODEL = load_yolo_model(model_name)

    try:
        results = YOLO_MODEL(image, imgsz=320)
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = YOLO_MODEL.names[cls]
                detections.append(
                    (label, float(conf), (int(x1), int(y1), int(x2 - x1), int(y2 - y1)))
                )

                # Create an alert for each detection
                Alert.objects.create(
                    camera=camera,
                    description=f"{label} detected with {conf:.2f} confidence",
                    severity="High" if label in ["gun", "knife"] else "Medium",
                )

        return detections
    except Exception as e:
        print(f"Error in object detection: {str(e)}")
        return []


def send_notification(alert):
    try:
        notification_settings = NotificationSettings.objects.get(user=alert.camera.user)

        if notification_settings.email_notifications:
            send_mail(
                "Security Alert",
                f"Alert from camera {alert.camera.name}: {alert.description}",
                settings.EMAIL_HOST_USER,
                [alert.camera.user.email],
                fail_silently=False,
            )
            print(f"Email notification sent to {alert.camera.user.email}")

        if notification_settings.telegram_notifications:
            telegram_bot_token = settings.TELEGRAM_BOT_TOKEN
            chat_id = notification_settings.telegram_chat_id
            message = f"Alert from camera {alert.camera.name}: {alert.description}"
            url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Telegram notification sent to chat ID {chat_id}")
            else:
                print(
                    f"Failed to send Telegram notification. Status code: {response.status_code}"
                )

        if notification_settings.whatsapp_notifications:
            whatsapp_number = notification_settings.whatsapp_number
            message = f"Alert from camera {alert.camera.name}: {alert.description}"
            # Implement WhatsApp notification logic here
            print(f"WhatsApp notification sent to {whatsapp_number}: {message}")

    except NotificationSettings.DoesNotExist:
        print(f"Notification settings not found for user {alert.camera.user.username}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
