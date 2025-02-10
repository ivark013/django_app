document.addEventListener('DOMContentLoaded', function() {
    initializeCameras();
    fetchNotificationSettings();
    setInterval(updateAlerts, 30000);
    setupLogout();
    document.getElementById('notificationForm').addEventListener('submit', updateNotificationSettings);
});

function initializeCameras() {
    const cameras = document.querySelectorAll('.camera-feed img');
    cameras.forEach(camera => {
        camera.addEventListener('error', () => handleCameraError(camera.dataset.cameraId));
    });
    updateCameraCount();
}

function updateCameraCount() {
    const activeCameras = document.querySelectorAll('.camera-feed img:not(.error)').length;
    document.getElementById('cameraCount').textContent = activeCameras;
}

function toggleCamera(cameraId) {
    const button = document.querySelector(`button[data-camera-id="${cameraId}"]`);
    const feedContainer = document.getElementById(`camera-feed-${cameraId}`);
    
    button.disabled = true;
    
    fetch(`/toggle_camera/${cameraId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        button.disabled = false;
        if (data.status !== undefined) {
            if (data.status) {
                // Camera is now active
                feedContainer.innerHTML = `
                    <img src="/video_feed/${cameraId}/" 
                         alt="Camera Feed" 
                         data-camera-id="${cameraId}"
                         onerror="handleCameraError('${cameraId}')">
                `;
                button.textContent = 'إيقاف';
            } else {
                // Camera is now inactive
                feedContainer.innerHTML = '<div class="camera-offline">الكاميرا غير متصلة</div>';
                button.textContent = 'تشغيل';
            }
            updateCameraCount();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.disabled = false;
        alert('حدث خطأ أثناء تغيير حالة الكاميرا');
    });
}

function handleCameraError(cameraId) {
    const feedContainer = document.getElementById(`camera-feed-${cameraId}`);
    if (feedContainer) {
        feedContainer.innerHTML = '<div class="camera-offline">الكاميرا غير متصلة</div>';
        updateCameraCount();
    }
}

function updateAlerts() {
    fetch('/get_latest_alerts/')
        .then(response => response.json())
        .then(data => {
            const alertsList = document.getElementById('alertsList');
            if (alertsList && data.alerts) {
                alertsList.innerHTML = data.alerts.map(alert => 
                    `<li>${alert.description} - ${alert.timestamp}</li>`
                ).join('');
            }
        })
        .catch(error => console.error('Error fetching alerts:', error));
}

function fetchNotificationSettings() {
    fetch('/get_notification_settings/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('emailNotifications').checked = data.emailNotifications;
            document.getElementById('telegramNotifications').checked = data.telegramNotifications;
            document.getElementById('whatsappNotifications').checked = data.whatsappNotifications;
        })
        .catch(error => console.error('Error fetching notification settings:', error));
}

function updateNotificationSettings(event) {
    event.preventDefault();
    
    const settings = {
        emailNotifications: document.getElementById('emailNotifications').checked,
        telegramNotifications: document.getElementById('telegramNotifications').checked,
        whatsappNotifications: document.getElementById('whatsappNotifications').checked
    };

    fetch('/update_notification_settings/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('تم حفظ الإعدادات بنجاح');
        } else {
            alert('حدث خطأ أثناء حفظ الإعدادات');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء حفظ الإعدادات');
    });
}

function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setupLogout() {
    const logoutForm = document.getElementById('logoutForm');
    if (logoutForm) {
        logoutForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (confirm('هل أنت متأكد أنك تريد تسجيل الخروج؟')) {
                this.submit();
            }
        });
    }
}

