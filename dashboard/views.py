import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.views.decorators import gzip
from django.conf import settings
from .models import Camera, Alert, NotificationSettings
from .utils import detect_objects, load_yolo_model, send_notification
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import threading
import time
import os
import json
from django.core.cache import cache
import requests
from django.core.mail import send_mail
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraStream:
    def __init__(self, camera_id):
        self.camera = Camera.objects.get(camera_id=camera_id)
        self.video = None
        self.model = load_yolo_model(
            "thief_mask"
        )  # Load the model when initializing the stream
        self.connect_camera()

    def connect_camera(self):
        try:
            cam_number = int(self.camera.camera_id.split("_")[1])
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]

            for backend in backends:
                self.video = cv2.VideoCapture(cam_number, backend)
                if self.video.isOpened():
                    logger.info(
                        f"Successfully opened camera {self.camera.camera_id} using backend {backend}"
                    )
                    break
                else:
                    logger.warning(
                        f"Failed to open camera {self.camera.camera_id} using backend {backend}"
                    )

            if not self.video.isOpened():
                raise ValueError(f"Failed to open camera {self.camera.camera_id}")

            # Set camera properties for better performance and wider view
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Increase width
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Increase height
            self.video.set(cv2.CAP_PROP_FPS, 30)
            self.video.set(cv2.CAP_PROP_BUFFERSIZE, 3)

            success, _ = self.video.read()
            if not success:
                raise ValueError("Failed to read test frame")

        except Exception as e:
            logger.error(f"Error initializing camera {self.camera.camera_id}: {str(e)}")
            self.video = None

    def get_frame(self):
        if self.video is None or not self.video.isOpened():
            self.connect_camera()
            if self.video is None:
                return None

        success, frame = self.video.read()
        if not success:
            logger.warning("Failed to read frame from camera.")
            self.video.release()
            self.video = None
            return None

        try:
            frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)

            # Apply zoom out effect
            height, width = frame.shape[:2]
            center = (width / 2, height / 2)
            scale_factor = 0.75  # Adjust this value to change the zoom level (less than 1 for zoom out)
            M = cv2.getRotationMatrix2D(center, 0, scale_factor)
            frame = cv2.warpAffine(frame, M, (width, height))

            detections = detect_objects(frame, "thief_mask", self.camera)

            for label, confidence, (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )

            _, jpeg = cv2.imencode(".jpg", frame)
            return jpeg.tobytes()
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return None

    def __del__(self):
        if self.video and self.video.isOpened():
            self.video.release()


def gen(camera_id):
    """Generate camera frames."""
    stream = CameraStream(camera_id)
    while True:
        frame = stream.get_frame()
        if frame is not None:
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )
        else:
            logger.warning("Received empty frame, attempting to reconnect...")
            time.sleep(1)  # Wait before trying again


@gzip.gzip_page
@login_required
def video_feed(request, camera_id):
    """Stream video from camera."""
    try:
        return StreamingHttpResponse(
            gen(camera_id), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except Exception as e:
        logger.error(f"Error in video streaming: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


@login_required
@require_POST
@csrf_exempt
def toggle_camera(request, camera_id):
    """Toggle camera active status."""
    try:
        camera = Camera.objects.get(camera_id=camera_id)
        camera.is_active = not camera.is_active
        camera.save()
        return JsonResponse({"status": camera.is_active})
    except Camera.DoesNotExist:
        return JsonResponse({"error": "Camera not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def alerts(request):
    """View all alerts."""
    alerts = Alert.objects.all().order_by("-timestamp")
    return render(request, "dashboard/alerts.html", {"alerts": alerts})


@login_required
@require_POST
def mark_alert_read(request, alert_id):
    """Mark an alert as read."""
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.is_read = True
        alert.save()
        return JsonResponse({"success": True})
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def notification_settings(request):
    """View and update notification settings."""
    settings, created = NotificationSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        try:
            settings.email_notifications = "email_notifications" in request.POST
            settings.telegram_notifications = "telegram_notifications" in request.POST
            settings.whatsapp_notifications = "whatsapp_notifications" in request.POST
            settings.telegram_chat_id = request.POST.get("telegram_chat_id", "")
            settings.whatsapp_number = request.POST.get("whatsapp_number", "")
            settings.save()
            return redirect("dashboard")
        except Exception as e:
            print(f"Error saving notification settings: {str(e)}")
            return render(
                request,
                "dashboard/notification_settings.html",
                {"settings": settings, "error": "Error saving settings"},
            )
    return render(
        request, "dashboard/notification_settings.html", {"settings": settings}
    )


@login_required
def get_latest_alerts(request):
    """Get latest unread alerts."""
    cache_key = f"latest_alerts_{request.user.id}"
    cached_alerts = cache.get(cache_key)

    if cached_alerts is None:
        alerts = Alert.objects.filter(is_read=False).order_by("-timestamp")[:5]
        alerts_data = [
            {
                "camera_name": alert.camera.name,
                "description": alert.description,
                "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for alert in alerts
        ]
        cache.set(cache_key, alerts_data, 60)  # Cache for 60 seconds
        return JsonResponse({"alerts": alerts_data})

    return JsonResponse({"alerts": cached_alerts})


@login_required
@require_POST
@csrf_exempt
def update_notification_settings(request):
    """Update notification settings via AJAX."""
    try:
        data = json.loads(request.body)
        settings, created = NotificationSettings.objects.get_or_create(
            user=request.user
        )

        settings.email_notifications = data.get("emailNotifications", False)
        settings.telegram_notifications = data.get("telegramNotifications", False)
        settings.whatsapp_notifications = data.get("whatsappNotifications", False)
        settings.telegram_chat_id = data.get("telegramUsername", "")
        settings.whatsapp_number = data.get("whatsappNumber", "")

        settings.save()
        return JsonResponse({"success": True})
    except Exception as e:
        print(f"Error updating notification settings: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def get_cameras(request):
    """Get list of active cameras."""
    try:
        cameras = Camera.objects.filter(is_active=True)
        camera_data = [
            {
                "id": camera.id,
                "name": camera.name,
                "camera_id": camera.camera_id,
                "is_active": camera.is_active,
            }
            for camera in cameras
        ]
        return JsonResponse({"cameras": camera_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def get_alerts(request):
    """Get recent alerts."""
    try:
        alerts = Alert.objects.all().order_by("-timestamp")[:10]
        alert_data = [
            {
                "id": alert.id,
                "camera_name": alert.camera.name,
                "description": alert.description,
                "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_read": alert.is_read,
                "severity": alert.severity,
            }
            for alert in alerts
        ]
        return JsonResponse({"alerts": alert_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def get_notification_settings(request):
    """Get current notification settings."""
    try:
        settings, created = NotificationSettings.objects.get_or_create(
            user=request.user
        )
        return JsonResponse(
            {
                "emailNotifications": settings.email_notifications,
                "telegramNotifications": settings.telegram_notifications,
                "whatsappNotifications": settings.whatsapp_notifications,
                "telegramUsername": settings.telegram_chat_id,
                "whatsappNumber": settings.whatsapp_number,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def custom_logout(request):
    """Logout user."""
    logout(request)
    return redirect("login")


@csrf_exempt
@require_POST
def chatbot(request):
    message = request.POST.get("message")
    if not message:
        return JsonResponse({"error": "No message provided"}, status=400)

    # Replace this with your chatbot API URL
    chatbot_api_url = "https://your-chatbot-api-url.com/chat"

    try:
        response = requests.post(chatbot_api_url, json={"message": message})
        response.raise_for_status()
        chatbot_response = response.json()
        return JsonResponse(chatbot_response)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_available_cameras():
    """Get list of available cameras connected to the system."""
    available_cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            camera_name = f"Camera {index}"
            camera_id = f"camera_{index}"
            available_cameras.append((camera_name, camera_id))
            cap.release()
        index += 1
    return available_cameras


def update_camera_database():
    """Update the database with currently available cameras."""
    available_cameras = get_available_cameras()
    current_camera_ids = set(Camera.objects.values_list("camera_id", flat=True))

    # Assume we're using the first user in the system for simplicity
    # In a real-world scenario, you'd want to associate cameras with specific users
    default_user = User.objects.first()

    for name, camera_id in available_cameras:
        camera, created = Camera.objects.get_or_create(
            camera_id=camera_id,
            defaults={
                "name": name,
                "user": default_user,  # Associate the camera with a user
            },
        )
        if not created:
            camera.name = name
            camera.is_active = True
            camera.save()
        current_camera_ids.discard(camera_id)

    # Set remaining cameras as inactive
    Camera.objects.filter(camera_id__in=current_camera_ids).update(is_active=False)


@login_required
def dashboard(request):
    """Main dashboard view."""
    update_camera_database()
    cameras = Camera.objects.filter(is_active=True)
    alerts = Alert.objects.filter(is_read=False).order_by("-timestamp")[:5]

    logger.info(f"Active cameras: {cameras.count()}")
    logger.info(f"Recent alerts: {alerts.count()}")

    return render(
        request, "dashboard/dashboard.html", {"cameras": cameras, "alerts": alerts}
    )
