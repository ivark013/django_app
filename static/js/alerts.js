document.addEventListener('DOMContentLoaded', function () {
    const markReadButtons = document.querySelectorAll('.mark-read-button');
    
    markReadButtons.forEach(button => {
        button.addEventListener('click', function () {
            const alertId = this.dataset.id;
            const alertItem = this.closest('.alert-item');

            // إضافة تأثير عند الضغط على زر القراءة
            button.textContent = 'جارٍ المعالجة...';
            button.disabled = true;

            fetch(`/api/mark-alert-read/${alertId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alertItem.classList.remove('unread');
                        alertItem.classList.add('read');
                        button.remove();
                    } else {
                        alert("لم يتم تحديث حالة التنبيه.");
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('حدث خطأ أثناء تحديث حالة التنبيه');
                });
        });
    });
});
