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

const animationEvent = whichAnimationEvent();

const inputCard = $("#input-card");
const inputRow = $("#input-row");
const preloader = $("#preloader");
const containerRow = $("#container-row");
const container = $("#container");
const refreshButton = $("#refresh");

let inputVisible = true;

function showContainerRow() {
    inputCard.off(animationEvent);

    inputRow.hide();
    containerRow.show();
}

function hideContainerRow() {
    inputRow.show();
    containerRow.hide();

    container.children().not('#preloader').remove();
}

function showCard() {
    hideContainerRow();

    inputCard
        .addClass("flipIn")
        .removeClass("flipOut");

    enableScanButton();
    hideRefreshButton();

    inputVisible = true;
}

function hideCard() {
    inputCard
        .removeClass("flipIn")
        .addClass("flipOut")
        .on(animationEvent, showContainerRow);

    inputVisible = false;

    preloader.show();
}

function disableScanButton() {
    scanButton.prop("disabled", true);
}

function enableScanButton() {
    scanButton.prop("disabled", false);
}

function showRefreshButton() {
    refreshButton.addClass("scale-in");
}

function hideRefreshButton() {
    refreshButton.removeClass("scale-in");
}

$(document).ready(() => {
    $(".button-collapse").sideNav();
    $(".modal").modal();

    refreshButton.click(() => {
        showCard();
    });
});