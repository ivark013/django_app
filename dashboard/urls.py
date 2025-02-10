from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("video_feed/<str:camera_id>/", views.video_feed, name="video_feed"),
    path("toggle_camera/<str:camera_id>/", views.toggle_camera, name="toggle_camera"),
    path("alerts/", views.alerts, name="alerts"),
    path(
        "mark_alert_read/<int:alert_id>/", views.mark_alert_read, name="mark_alert_read"
    ),
    path(
        "notification_settings/",
        views.notification_settings,
        name="notification_settings",
    ),
    path("get_latest_alerts/", views.get_latest_alerts, name="get_latest_alerts"),
    path(
        "update_notification_settings/",
        views.update_notification_settings,
        name="update_notification_settings",
    ),
    path("get_cameras/", views.get_cameras, name="get_cameras"),
    path("get_alerts/", views.get_alerts, name="get_alerts"),
    path(
        "get_notification_settings/",
        views.get_notification_settings,
        name="get_notification_settings",
    ),
    path("logout/", views.custom_logout, name="logout"),
    path("chatbot/", views.chatbot, name="chatbot"),
]
