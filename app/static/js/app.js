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

function openModal(title, text) {
    $("#modal-title").text(title);
    $("#modal-text").text(text);

    $(".modal").modal("open");
}

function getUser(userId) {
    return promiseGet("api/user", {userId});
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

const inputCard = $("#input-card");
const inputRow = $("#input-row");
const containerRow = $("#container-row");
const preloader = $("#preloader");

function showContainerRow() {
    inputRow.hide();
    containerRow.show();
}

function hideContainerRow() {
    inputRow.show();
    containerRow.hide();
}

function showCard() {
    hideContainerRow();

    inputCard
        .addClass("flipIn")
        .removeClass("flipOut");
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
    inputCard
        .removeClass("flipIn")
        .addClass("flipOut")
        .one(whichAnimationEvent(), () => {
            showContainerRow();
        });
}