function drawGraph(nodes, edges) {
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
        .legend(false)
        .data(nodes)
        .edges(edges)
        .id("id")
        .text("name")
        .icon("photo")
        .color("color")
        .draw();
}

function getMutualFriends(user) {
    return promiseGet("api/mutual_friends", {userId: user.id});
}

const userIdInput = $("#userId");

function checkInputField() {
    scanButton.prop("disabled", userIdInput.val() === "");
}

$(document).ready(() => {
    checkInputField();
    userIdInput.on("change propertychange keydown keyup cut paste click input", checkInputField);

    scanButton.click(() => {
        disableScanButton();

        getUser(userIdInput.val())
            .then((user) => {
                hideCard();
                showRefreshButton();

                getMutualFriends(user)
                    .then((response) => {
                        if (inputVisible) {
                            return;
                        }

                        const nodes = response.friends.concat(user);
                        const edges = response.connections;
                        for (const friend of response.friends) {
                            edges.push({
                                source: user.id,
                                target: friend.id
                            });
                        }

                        showContainerRow();

                        preloader.hide();
                        drawGraph(nodes, edges);
                    })
                    .catch((message) => {
                        if (inputVisible) {
                            return;
                        }

                        catchError(message);
                        showCard();
                    });
            })
            .catch((message) => {
                catchError(message);
                enableScanButton();
            });
    });
});