$(document).ready(() => {
    const userIdInput = $("#userId");
    const scanButton = $("#scan");

    userIdInput.on('input propertychange paste', () => {
        scanButton.prop("disabled", userIdInput.val() === "")
    });

    scanButton.click(() => {
        getUser($("#userId").val())
            .then(user => {
                hideCard();

                getMutualFriends(user)
                    .then(response => {
                        const nodes = response.friends.concat(user);
                        const edges = response.friends_connections;
                        for (const friend of response.friends) {
                            edges.push({
                                source: user.id,
                                target: friend.id
                            });
                        }

                        return drawGraph(nodes, edges);
                    })
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

function getUser(user_id) {
    return promiseGet("api/user", {user_id: user_id});
}

function getMutualFriends(user) {
    return promisePost("api/mutual_friends", JSON.stringify(user));
}

//TODO возможность возврата к панели ввода ID
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