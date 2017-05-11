function drawGraph(userId, nodes, edges) {
    d3plus.viz()
        .type("network")
        .format({
            "text": (text) => {
                if (text === "primary connections") {
                    return "Друзья";
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
        .focus(userId)
        .id("id")
        .text("name")
        .icon("photo")
        .draw(() => $("#preloader").hide())
        .draw(() => {
        });
}

function getMutualFriends(user) {
    return promiseGet("api/mutual_friends", {user_id: user.id});
}

$(document).ready(() => {
    const userIdInput = $("#userId");
    const scanButton = $("#scan");

    userIdInput.on("change propertychange keydown keyup cut paste click input", () => {
        scanButton.prop("disabled", userIdInput.val() === "");
    });

    scanButton.click(() => {
        scanButton.prop("disabled", true);

        getUser(userIdInput.val())
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

                        drawGraph(user.id, nodes, edges);
                    });
            })
            .catch((message) => {
                catchError(message);
                scanButton.prop("disabled", false);
            });
    });
});