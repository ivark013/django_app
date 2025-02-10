document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('notificationForm');
    const telegramCheck = document.getElementById('telegramNotifications');
    const whatsappCheck = document.getElementById('whatsappNotifications');
    const telegramInput = document.getElementById('telegramInputGroup');
    const whatsappInput = document.getElementById('whatsappInputGroup');
    
    // Initial state
    toggleInputVisibility(telegramCheck, telegramInput);
    toggleInputVisibility(whatsappCheck, whatsappInput);
    
    // Event listeners
    telegramCheck.addEventListener('change', () => toggleInputVisibility(telegramCheck, telegramInput));
    whatsappCheck.addEventListener('change', () => toggleInputVisibility(whatsappCheck, whatsappInput));
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        fetch('/update_notification_settings/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                emailNotifications: formData.get('email_notifications') === 'on',
                telegramNotifications: formData.get('telegram_notifications') === 'on',
                whatsappNotifications: formData.get('whatsapp_notifications') === 'on',
                telegramUsername: formData.get('telegram_chat_id'),
                whatsappNumber: formData.get('whatsapp_number')
            })
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
    });
});

function toggleInputVisibility(checkbox, inputGroup) {
    inputGroup.style.display = checkbox.checked ? 'block' : 'none';
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

