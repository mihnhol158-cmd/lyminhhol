// បិទ Alert message ដោយស្វ័យប្រវត្តក្រោយ 5 វិនាទី
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.remove();
        });
    }, 5000);
});
