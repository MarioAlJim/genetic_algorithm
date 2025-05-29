function downloadReport() {
    fetch('/playground/download')
        .then( res => res.blob() )
        .then( blob => {
            let file = window.URL.createObjectURL(blob);
            window.open(file, '_blank');
        });
}