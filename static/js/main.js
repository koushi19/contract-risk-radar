document.addEventListener('DOMContentLoaded', function() {
    const pdfInput = document.getElementById('file_pdf');
    const txtInput = document.getElementById('file_txt');

    if (pdfInput) {
        pdfInput.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.files.length > 0) {
                label.innerHTML = `<span style="color: #10b981;">✓ ${this.files[0].name}</span>`;
                label.style.borderColor = '#10b981';
            }
        });
    }

    if (txtInput) {
        txtInput.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.files.length > 0) {
                label.innerHTML = `<span style="color: #10b981;">✓ ${this.files[0].name}</span>`;
                label.style.borderColor = '#10b981';
            }
        });
    }
});
