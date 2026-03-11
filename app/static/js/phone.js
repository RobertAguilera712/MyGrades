function initPhoneFields() {
    $('input[type="tel"]').each(function () {
        $(this).mask("000-000-0000");
    });
}

// full page load
document.addEventListener("DOMContentLoaded", function () {
    initPhoneFields();
});

// HTMX swap
document.body.addEventListener("htmx:afterSwap", function (evt) {
    if (evt.target.id === "module") {
        setTimeout(initPhoneFields, 50);
    }
});