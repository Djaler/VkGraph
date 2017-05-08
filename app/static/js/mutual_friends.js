$(document).ready(() => {
    $("#scan").click(() => {
        //TODO проверка на отсутствие ID
        getUser($("#userId").val())
            .then(user => {
                hideCard();

                getMutualFriends(user)
                    .then(response => drawGraph(response.nodes, response.edges))
                //TODO Проверка на количество друзей
            })
            .catch(message => {
                if (message === "NO_USER") {
                    return alert("Пользователя с таким ID не существует");
                } else if (message === "USER_DEACTIVATED") {
                    return alert("Пользователь деактивирован");
                }
            });
    });
});

function drawGraph(nodes, edges) {
    d3plus.viz()
        .type("network")
        .format({
            "text": text => {
                if (text === "primary connections") {
                    return "Общие друзья";
                } else {
                    return text;
                }
            }
        })
        .messages("Загрузка...")
        .container("#container")
        .width({small: 700})
        .resize(true)
        .data(nodes)
        .edges(edges)
        .id("id")
        .text("name")
        .icon("photo")
        .draw(() => $("#preloader").hide())
        .draw(() => {
        });
}

function getUser(user_id) {
    return promiseGet("api/user", {user_id: user_id});
}

function getMutualFriends(user) {
    return promisePost("api/mutual_friends", JSON.stringify(user));
}

function showCard() {
    $("#input-row").show();
    $("#container-row").addClass("hidden");

    $('.card-panel').toggleClass('flipIn');
}

function hideCard() {
    $('.card-panel')
        .toggleClass('flipIn')
        .one(whichAnimationEvent(), () => {
            $("#input-row").hide();
            $("#container-row").removeClass("hidden");
        });
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
        if (el.style[animation] !== undefined) {
            return animations[animation];
        }
    }
}