function downloadReport() {
    fetch('/playground/download')
        .then( res => res.blob() )
        .then( blob => {
            var file = window.URL.createObjectURL(blob);
        window.open(file, '_blank');
        });
}