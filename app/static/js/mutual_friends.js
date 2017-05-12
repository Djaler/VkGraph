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
        .data(nodes)
        .edges(edges)
        .id("id")
        .text("name")
        .icon("photo")
        .draw();
}

function getMutualFriends(user) {
    return promiseGet("api/mutual_friends", {userId: user.id});
}

const scanButton = $("#scan");
const userIdInput = $("#userId");

function checkInputField() {
    scanButton.prop("disabled", userIdInput.val() === "");
}

$(document).ready(() => {
    checkInputField();
    userIdInput.on("change propertychange keydown keyup cut paste click input", checkInputField);

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

                        inputRow.hide();
                        containerRow.show();

                        preloader.hide();
                        drawGraph(nodes, edges);
                    })
                    .catch((message) => {
                        catchError(message);
                        scanButton.prop("disabled", false);
                    });
            })
            .catch((message) => {
                catchError(message);
                scanButton.prop("disabled", false);
            });
    });
});