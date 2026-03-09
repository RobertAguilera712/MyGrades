function initDataTable() {
    const table = $('#mainTable');

    if (!table.length) return;

    if ($.fn.DataTable.isDataTable('#mainTable')) {
        $('#mainTable').DataTable().destroy();
    }

    $('#mainTable').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
        }
    });
}

// full page load
document.addEventListener("DOMContentLoaded", function () {
    initDataTable();
});


// HTMX swap
document.body.addEventListener("htmx:afterSwap", function (evt) {
    if (evt.target.id === "module") {
        setTimeout(initDataTable, 50);
    }
});