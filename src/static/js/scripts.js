function downloadReport() {
    fetch('/playground/download')
        .then( res => res.blob() )
        .then( blob => {
            let file = window.URL.createObjectURL(blob);
            window.open(file, '_blank');
        });
}

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("config-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        if (form.checkValidity()) {
            document.getElementById("loader-modal").classList.add('loader-modal--active');
            form.submit();
        } else {
            form.reportValidity();
            document.getElementById("loader-modal").classList.remove('loader-modal--active');
        }
    });
});

