function toggleConfigForm() {
    var algorithm = document.querySelector('select[name="algorithm"]').value;
    var configFormContainer = document.getElementById('configFormContainer');

    if (algorithm === 'algorithm_1') {
        configFormContainer.style.display = 'block';
        document.getElementById('config-form').style.display = 'block';
    } else {
        configFormContainer.style.display = 'none';

    }
}
window.onload = toggleConfigForm;

function downloadReport() {
    fetch('/playground/download')
        .then( res => res.blob() )
        .then( blob => {
            var file = window.URL.createObjectURL(blob);
        window.open(file, '_blank');
        });
}