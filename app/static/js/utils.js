function promiseGet(url, data) {
    return new Promise((resolve, reject) => {
        $.get(url, data)
            .done((response) => (response.status === "OK") ? resolve(response.data) : reject(response.data))
            .fail(() => reject());
    });
}

function getUser(userId) {
    return promiseGet("api/user", {userId});
}