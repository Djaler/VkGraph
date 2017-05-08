$(document).ready(() => {
    $(".button-collapse").sideNav();
});

function promiseGet(url, data) {
    return new Promise((resolve, reject) => {
        $.get(url, data)
            .done(response => (response.status === "OK") ? resolve(response.data) : reject(response.data))
            .fail(() => reject());
    })
}

function promisePost(url, data) {
    return new Promise((resolve, reject) => {
        $.post({
            url: url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: data
        })
            .done(response => (response.status === "OK") ? resolve(response.data) : reject(response.data))
            .fail(() => reject());
    });
}