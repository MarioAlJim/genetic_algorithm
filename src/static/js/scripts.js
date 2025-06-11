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

document.addEventListener("DOMContentLoaded", function () {
    // Open modal on help button click
    document.querySelectorAll(".help-button").forEach(button => {
        const targetId = button.getAttribute("data-modal-target");
        button.addEventListener("click", () => {
            document.getElementById(targetId).classList.add("help-modal--active");
        });
    });

    // Close modal on close button click
    document.querySelectorAll(".help-modal__close").forEach(span => {
        const targetId = span.getAttribute("data-modal-target");
        span.addEventListener("click", () => {
            document.getElementById(targetId).classList.remove("help-modal--active");
        });
    });

    // Close modal on outside click
    window.addEventListener("click", event => {
        if (event.target.classList.contains("help-modal")) {
            event.target.classList.remove("help-modal--active");
        }
    });
});

function showNotification(message, type='info') {
    const container = document.getElementById("notification-container");
    const notification = document.createElement("div");
    notification.className = `notification--${type}`;
    notification.classList.add('notification');
    notification.textContent = message;

    container.appendChild(notification);
    void notification.offsetWidth;
    notification.classList.add('notification--show');

    const autoHideTimer = setTimeout(() => {
        hideNotification(notification);
    }, 5000);

    notification.addEventListener('click', () => {
        clearTimeout(autoHideTimer);
        hideNotification(notification);
    });
}

function hideNotification(notification) {
    notification.classList.remove('notification--show');
    setTimeout(() => {
        notification.remove();
    }, 300);
}