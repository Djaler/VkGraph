$(document).ready(() => {
    $(".button-collapse").sideNav();
    $(".modal").modal();
});

function promiseGet(url, data) {
    return new Promise((resolve, reject) => {
        $.get(url, data)
            .done((response) => (response.status === "OK") ? resolve(response.data) : reject(response.data))
            .fail(() => reject());
    });
}

function promisePost(url, data) {
    return new Promise((resolve, reject) => {
        $.post({
            url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data
        })
            .done((response) => (response.status === "OK") ? resolve(response.data) : reject(response.data))
            .fail(() => reject());
    });
}

function openModal(title, text) {
    $("#modal-title").text(title);
    $("#modal-text").text(text);

    $(".modal").modal("open");
}