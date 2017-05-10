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

function getUser(userId) {
    return promiseGet("api/user", {user_id: userId});
}

function catchError(message) {
    let text;
    if (typeof message === "undefined") {
        text = "Произошла непредвиденная ошибка";
    } else {
        text = message;
    }
    openModal("Ошибка", text);
}

//TODO возможность возврата к панели ввода ID
function showCard() {
    $("#input-row").show();
    $("#container-row").addClass("hidden");

    $(".card-panel").toggleClass("flipIn");
}

function whichAnimationEvent() {
    const el = document.createElement("fakeelement");

    const animations = {
        "animation": "animationend",
        "OAnimation": "oAnimationEnd",
        "MozAnimation": "animationend",
        "WebkitAnimation": "webkitAnimationEnd"
    };

    for (let animation in animations) {
        if (typeof el.style[animation] !== "undefined") {
            return animations[animation];
        }
    }
}

function hideCard() {
    $(".card-panel")
        .toggleClass("flipIn")
        .one(whichAnimationEvent(), () => {
            $("#input-row").hide();
            $("#container-row").removeClass("hidden");
        });
}