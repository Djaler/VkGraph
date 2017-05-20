const inputCard = $("#input-card");
const inputRow = $("#input-row");
const scanButton = $("#scan");
const preloader = $("#preloader");
const containerRow = $("#container-row");
const container = $("#container");
const refreshButton = $("#refresh");

let inputVisible = true;

const animationEvent = (function () {
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
}());

function openModal(title, text) {
    $("#modal-title").text(title);
    $("#modal-text").text(text);

    $(".modal").modal("open");
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

function showContainerRow() {
    inputCard.off(animationEvent);

    inputRow.hide();
    containerRow.show();
}

function hideContainerRow() {
    inputRow.show();
    containerRow.hide();

    container.children().not("#preloader").remove();
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

$(document).ready(() => {
    $(".button-collapse").sideNav();
    $(".modal").modal();

    refreshButton.click(() => {
        showCard();
    });
});