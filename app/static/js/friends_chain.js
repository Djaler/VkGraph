const chainContainer = $(".chain-container");

function getFriendsChain(user1, user2, chainLength) {
    return promiseGet("api/friends_chain", {user1Id: user1.id, user2Id: user2.id, chainLength});
}

function displayChain(users) {
    const elementTemplate = $("#chain-element-template").html();
    const arrow = $($("#chain-arrow-template").html());

    for (let i = 0; i < users.length; i++) {
        const user = users[i];

        const node = $(elementTemplate);
        node.find(".chain-element-image").attr("src", user.photo);
        node.find(".chain-element-link").attr("href", user.link);
        node.find(".chain-element-link").text(user.name);
        chainContainer.append(node);

        if (i < users.length - 1) {
            chainContainer.append(arrow.clone());
        }
    }
}

$(document).ready(() => {
    const userId1Input = $("#userId1");
    const userId2Input = $("#userId2");
    const scanButton = $("#scan");

    userId1Input.add(userId2Input).on("change propertychange keydown keyup cut paste click input", () => {
        let disabled = false;

        if (userId1Input.val() === "" || userId2Input.val() === "") {
            disabled = true;
        } else if (userId1Input.val() === userId2Input.val()) {
            disabled = true;
        }

        scanButton.prop("disabled", disabled);
    });

    scanButton.click(() => {
        scanButton.prop("disabled", true);

        Promise.all([getUser(userId1Input.val()), getUser(userId2Input.val())])
            .then((users) => {
                const [user1, user2] = users;

                if (user1.id === user2.id) {
                    catchError("Введенные пользователи имеют одинаковый Id");
                    scanButton.prop("disabled", false);
                    return;
                }

                hideCard();

                getFriendsChain(user1, user2, 5)
                    .then((response) => {
                        if (response === null) {
                            catchError("Не удалось найти цепочку");
                            showCard();
                            scanButton.prop("disabled", false);
                            return;
                        }
                        $("#preloader").hide();
                        displayChain([user1].concat(response).concat([user2]));
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