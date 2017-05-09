function drawGraph(nodes, edges) {
    d3plus.viz()
        .type("network")
        .format({
            "text": (text) => {
                if (text === "primary connections") {
                    return "Общие друзья";
                } else {
                    return text;
                }
            }
        })
        .messages("Загрузка...")
        .container("#container")
        .background("#eeeeee")
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

function getUser(userId) {
    return promiseGet("api/user", {user_id: userId});
}

function getMutualFriends(user) {
    return promisePost("api/mutual_friends", JSON.stringify(user));
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

$(document).ready(() => {
    const userIdInput = $("#userId");
    const scanButton = $("#scan");

    userIdInput.on("change propertychange keydown keyup cut paste click input", () => {
        scanButton.prop("disabled", userIdInput.val() === "");
    });

    scanButton.click(() => {
        scanButton.prop("disabled", true);

        getUser($("#userId").val())
            .then((user) => {
                hideCard();

                getMutualFriends(user)
                    .then((response) => {
                        const nodes = response.friends.concat(user);
                        const edges = response.friends_connections;
                        for (const friend of response.friends) {
                            edges.push({
                                source: user.id,
                                target: friend.id
                            });
                        }

                        return drawGraph(nodes, edges);
                    });
            })
            .catch((message) => {
                let text;
                if (message === "NO_USER") {
                    text = "Пользователя с таким ID не существует";
                } else if (message === "USER_DEACTIVATED") {
                    text = "Пользователь деактивирован";
                } else if (message === "NO_FRIENDS") {
                    text = "У пользователя отсутствуют или скрыты друзья";
                } else {
                    text = "Произошла непредвиденная ошибка";
                }
                openModal("Ошибка", text);
                scanButton.prop("disabled", false);
            });
    });
});