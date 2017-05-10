function getFriendsChain(user1, user2, chainLength) {
    return promiseGet("api/friends_chain", {user1Id: user1.id, user2Id: user2.id, chainLength: chainLength});
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

        getUser(userId1Input.val())
            .then((user1) => {
                getUser(userId2Input.val())
                    .then((user2) => {
                        if (user1.id === user2.id) {
                            catchError("Введенные пользователи имеют одинаковый Id");
                            return;
                        }

                        hideCard();

                        getFriendsChain(user1, user2, 5)
                            .then((response) => {
                                if (response === null) {
                                    catchError("Не удалось найти цепочку");
                                    showCard();
                                    return;
                                }
                                console.log(response);
                            })
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