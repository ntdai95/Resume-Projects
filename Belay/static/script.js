/* For auth */


function signup() {
    let username = document.getElementById("usernamesignup").value;
    let password = document.getElementById("passwordsignup").value;
    let magiclink = localStorage.getItem("ntdai95_belay_magiclink");

    fetch("http://127.0.0.1:5000/api/user", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, password: password})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            localStorage.setItem('ntdai95_belay_authkey', data.authkey);
            localStorage.setItem('ntdai95_belay_username', username);

            history.state["authkey"] = data.authkey;
            history.state["username"] = username;
            let pushStateState = history.state;
            let pushStateUnused = null;
            let pushStateUrl = null;
            if (magiclink !== null && magiclink !== "null") {
                pushStateUnused = "User Entered Page";
                pushStateUrl = magiclink;
                localStorage.setItem('ntdai95_belay_magiclink', null);
            } else {
                pushStateUnused = "Channels Page";
                pushStateUrl = "http://127.0.0.1:5000/channel";
            }

            checkState(true, pushStateState, pushStateUnused, pushStateUrl);
        } else {
            alert("Username has been used!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById("usernamesignup").value = "";
    document.getElementById("passwordsignup").value = "";
    document.getElementById("usernamelogin").value = "";
    document.getElementById("passwordlogin").value = "";

    return;
}


function login() {
    let username = document.getElementById("usernamelogin").value;
    let password = document.getElementById("passwordlogin").value;
    let magiclink = localStorage.getItem("ntdai95_belay_magiclink");

    fetch("http://127.0.0.1:5000/api/user?username=" + username + "&password=" + password, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            localStorage.setItem('ntdai95_belay_authkey', data.authkey);
            localStorage.setItem('ntdai95_belay_username', username);
            history.state["authkey"] = data.authkey;
            history.state["username"] = username;

            let pushStateState = history.state;
            let pushStateUnused = null;
            let pushStateUrl = null;

            if (magiclink !== null && magiclink !== "null") {
                pushStateUnused = "User Entered Page";
                pushStateUrl = magiclink;
                localStorage.setItem('ntdai95_belay_magiclink', null);
            } else {
                pushStateUnused = "Channels Page";
                pushStateUrl = "http://127.0.0.1:5000/channel";
            }

            checkState(true, pushStateState, pushStateUnused, pushStateUrl);
        } else {
            alert("Wrong username and password combination!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById("usernamesignup").value = "";
    document.getElementById("passwordsignup").value = "";
    document.getElementById("usernamelogin").value = "";
    document.getElementById("passwordlogin").value = "";

    return;
}


function createChannel() {
    let channelName = encodeURIComponent(document.getElementById("newChannelName").value);
    let authkey = localStorage.getItem("ntdai95_belay_authkey");

    fetch("http://127.0.0.1:5000/api/channel", {
        method: 'POST',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'},
        body: JSON.stringify({channelName: channelName})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == false) {
            alert("You don't have a valid authentication key!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById("newChannelName").value = "";

    return;
}


function getChannels() {
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let promise = fetch("http://127.0.0.1:5000/api/channel", {
        method: 'GET',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'}
    })

    return promise;
}


function startChannelPolling() {
    let promiseChannels = getChannels();

    promiseChannels
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            document.querySelector(".channelColumn h1").innerHTML = "Welcome, " + localStorage.getItem('ntdai95_belay_username') + "!";
            let channelTable = document.getElementsByClassName("channelTable");
            let channels = data.channels;

            if (channels.length > 0) {
                for (let i = 0; i < channels.length; i++) {
                    if (document.querySelector("#channel" + channels[i][0]) == null) {
                        let tr = document.createElement('tr');
                        tr.setAttribute("id", "rowChannel_id" + channels[i][0]);
                        let td = document.createElement('td');
                        let button = document.createElement('button');
                        button.setAttribute("type", "button");
                        button.setAttribute("id", "channel" + channels[i][0]);
                        button.setAttribute("value", "Go");
                        button.setAttribute("onclick", "goToChannel('" + channels[i][0] + "');");

                        button.innerHTML = decodeURIComponent(channels[i][1]);
                        td.appendChild(button);
                        tr.appendChild(td);
                        channelTable[0].appendChild(tr);
                    }
                }
            }
        } else {
            alert("You don't have a valid authentication key!");
        }

        if (window.location.pathname.startsWith('/channel')) {
            startCountPolling();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return;
}


function getUnreadMessageCounts() {
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let username = localStorage.getItem('ntdai95_belay_username');
    let promise = fetch("http://127.0.0.1:5000/api/message/unread?username=" + username, {
        method: 'GET',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'}
    })

    return promise;
}


function startCountPolling() {
    let promiseCounts = getUnreadMessageCounts();

    promiseCounts
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            let channel_idCounts = data.channel_idCounts;

            if (channel_idCounts.length > 0) {
                for (let i = 0; i < channel_idCounts.length; i++) {
                    if (document.querySelector("#unreadMessageCount" + channel_idCounts[i][0]) == null) {
                        let tr = document.querySelector("#rowChannel_id" + channel_idCounts[i][0]);

                        if (tr != null) {
                            let td = document.createElement('td');
                            td.setAttribute("id", "unreadMessageCount" + channel_idCounts[i][0]);
                            let p = document.createElement('p');
                            p.innerHTML = channel_idCounts[i][1] + " new message(s)";

                            td.appendChild(p);
                            tr.appendChild(td);
                        }
                    } else {
                        let td = document.querySelector("#unreadMessageCount" + channel_idCounts[i][0]);
                        td.innerHTML = "";
                        let p = document.createElement('p');
                        p.innerHTML = channel_idCounts[i][1] + " new message(s)";

                        td.appendChild(p);
                    }
                }
            }
        } else {
            alert("You don't have a valid authentication key!");
        }

        if (window.location.pathname.startsWith('/channel')) {
            startChannelPolling();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return;
}


function goToChannel(channel_id) {
    history.state["channel_id"] = channel_id;
    let pushStateState = history.state;
    let pushStateUnused = "Channel Page";
    let pushStateUrl = "http://127.0.0.1:5000/channel/" + channel_id;

    checkState(true, pushStateState, pushStateUnused, pushStateUrl);

    return;
}


function postMessage() {
    let newMessage = encodeURIComponent(document.getElementById("newMessage").value);
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let username = localStorage.getItem('ntdai95_belay_username');

    fetch("http://127.0.0.1:5000/api/channel/" + history.state["channel_id"] + "/message", {
        method: 'POST',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'},
        body: JSON.stringify({newMessage: newMessage, username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == false) {
            alert("You don't have a valid authentication key!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById("newMessage").value = "";

    return;
}


function updateUnreadMessageCounts(channel_id, message_id) {
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let username = localStorage.getItem('ntdai95_belay_username');

    fetch("http://127.0.0.1:5000/api/message/unread", {
        method: 'POST',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, channel_id: channel_id, message_id: message_id})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == false) {
            alert("You don't have a valid authentication key!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return;
}


function getMessages() {
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let promise = fetch("http://127.0.0.1:5000/api/channel/" + history.state["channel_id"] + "/message", {
        method: 'GET',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'}
    });

    return promise;
}


function startMessagePolling() {
    let promise = getMessages();

    promise
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            let messageContent = document.querySelector(".messageContent");
            let messages = data.messages;

            if (document.querySelector("#channelID" + history.state["channel_id"]) == null || messageContent.length != messages.length) {
                messageContent.innerHTML = "";
            }

            if (messages.length > 0) {
                for (let i = 0; i < messages.length; i++) {
                    if (document.querySelector("#message" + messages[i][0]) == null) {
                        let div = document.createElement('div');
                        div.setAttribute("class", "post");
                        div.setAttribute("id", "channelID" + messages[i][4]);
                        let message = document.createElement('message');
                        message.setAttribute("id", "message" + messages[i][0]);
                        let author = document.createElement('author');
                        author.innerHTML = messages[i][2];
                        let content = document.createElement('content');
                        let text = decodeURIComponent(messages[i][1]);
                        let urls = getImageURLs(text);

                        if (urls) {
                            for (let i = 0; i < urls.length; i++) {
                                text = text.replace(urls[i][0], "");
                            }

                            content.innerHTML = text;

                            for (let i = 0; i < urls.length; i++) {
                                let p = document.createElement("p");
                                let img = document.createElement("img");
                                img.setAttribute("src", urls[i][0]);
                                p.appendChild(img);
                                content.appendChild(p);
                            }
                        } else {
                            content.innerHTML = text;
                        }

                        let button = document.createElement('button');
                        button.setAttribute("class", "messageThread");
                        button.setAttribute("type", "button");
                        button.setAttribute("value", "Reply");
                        button.setAttribute("onclick", "goToThread('" + messages[i][0] + "');");
                        button.innerHTML = "Replies: " + messages[i][3];

                        message.appendChild(author);
                        message.appendChild(content);
                        message.appendChild(button);
                        div.appendChild(message);
                        messageContent.appendChild(div);
                    } else if (document.querySelector("#message" + messages[i][0] + " button").innerHTML != "Replies: " + messages[i][3]) {
                        document.querySelector("#message" + messages[i][0] + " button").innerHTML = "Replies: " + messages[i][3];
                    }
                }

                updateUnreadMessageCounts(messages[messages.length - 1][4], messages[messages.length - 1][0]);
            }
        } else {
            alert("You don't have a valid authentication key!");
        }

        if (window.location.pathname.startsWith('/channel/') && window.location.pathname.includes('/thread/') == false) {
            startMessagePolling();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return;
}


function goToThread(message_id) {
    history.state["message_id"] = message_id;
    let pushStateState = history.state;
    let pushStateUnused = "Thread Page";
    let pushStateUrl = "http://127.0.0.1:5000/channel/" + history.state['channel_id'] + "/thread/" + message_id;

    checkState(true, pushStateState, pushStateUnused, pushStateUrl);

    return;
}


function replyMessage() {
    let newReply = encodeURIComponent(document.getElementById("newReply").value);
    let username = localStorage.getItem('ntdai95_belay_username');
    let authkey = localStorage.getItem("ntdai95_belay_authkey");

    fetch("http://127.0.0.1:5000/api/channel/" + history.state["channel_id"] + "/message/" + history.state["message_id"], {
        method: 'POST',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'},
        body: JSON.stringify({newReply: newReply, username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == false) {
            alert("You don't have a valid authentication key!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    document.getElementById("newReply").value = "";

    return;
}


function getReplies() {
    let authkey = localStorage.getItem("ntdai95_belay_authkey");
    let promise = fetch("http://127.0.0.1:5000/api/channel/" + history.state["channel_id"] + "/message/" + history.state["message_id"], {
        method: 'GET',
        headers: {'Authorization': authkey, 'Content-Type': 'application/json'}
    })
    
    return promise;
}


function startReplyPolling() {
    let promise = getReplies();

    promise
    .then(response => response.json())
    .then(data => {
        if (data.success == true) {
            let threadContentPost = document.querySelector(".threadContent .post");

            if (threadContentPost.getAttribute("id") != data.message[0]) {
                threadContentPost.setAttribute("id", "");
                threadContentPost.innerHTML = "";

                let h3Message = document.createElement('h3');
                h3Message.innerHTML = "Message:";
                let message = document.createElement('message');
                let author = document.createElement('author');
                author.innerHTML = data.message[2];
                let content = document.createElement('content');
                let text = decodeURIComponent(data.message[1]);
                let urls = getImageURLs(text);

                if (urls) {
                    for (let i = 0; i < urls.length; i++) {
                        text = text.replace(urls[i][0], "");
                    }

                    content.innerHTML = text;

                    for (let i = 0; i < urls.length; i++) {
                        let p = document.createElement("p");
                        let img = document.createElement("img");
                        img.setAttribute("src", urls[i][0]);
                        p.appendChild(img);
                        content.appendChild(p);
                    }
                } else {
                    content.innerHTML = text;
                }

                let button = document.createElement('button');
                button.setAttribute("class", "replyThread");
                button.setAttribute("type", "button");
                button.setAttribute("value", "Go");
                button.setAttribute("onclick", "goToChannel('" + data.message[3] + "');");
                button.innerHTML = "Go To Channel";
                let h3Replies = document.createElement('h3');
                h3Replies.innerHTML = "Replies:";

                threadContentPost.appendChild(h3Message);
                message.appendChild(author);
                message.appendChild(content);
                message.appendChild(button);
                threadContentPost.appendChild(message);
                threadContentPost.appendChild(h3Replies);
            }

            if (threadContentPost.getAttribute("id") == "") {
                threadContentPost.setAttribute("id", data.message[0]);
            }

            if (document.querySelector(".threadContent .post .messageReply") == null) {
                let div = document.createElement('div');
                div.setAttribute("class", "messageReply");
                threadContentPost.appendChild(div);
            }

            let messageReply = document.querySelector(".threadContent .post .messageReply");
            messageReply.innerHTML = "";
            let replies = data.replies;

            if (replies.length > 0) {
                for (let i = 0; i < replies.length; i++) {
                    if (document.querySelector(".threadContent .post .messageReply #reply_id" + replies[i][0]) == null) {
                        let message = document.createElement('message');
                        message.setAttribute("id", "reply_id" + replies[i][0]);
                        let author = document.createElement('author');
                        author.innerHTML = replies[i][2];
                        let content = document.createElement('content');
                        let text = decodeURIComponent(replies[i][1]);
                        let urls = getImageURLs(text);

                        if (urls) {
                            for (let i = 0; i < urls.length; i++) {
                                text = text.replace(urls[i][0], "");
                            }

                            content.innerHTML = text;

                            for (let i = 0; i < urls.length; i++) {
                                let p = document.createElement("p");
                                let img = document.createElement("img");
                                img.setAttribute("src", urls[i][0]);
                                p.appendChild(img);
                                content.appendChild(p);
                            }
                        } else {
                            content.innerHTML = text;
                        }

                        message.appendChild(author);
                        message.appendChild(content);
                        messageReply.appendChild(message);
                    }
                }
            }
        } else {
            alert("You don't have a valid authentication key!");
        }

        if (window.location.pathname.includes('/thread/')) {
            startReplyPolling();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return;
}


/* For all */


function getImageURLs(message) {
    const regex = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpeg|jpg|gif|png)+/g;
    let array = [...message.matchAll(regex)];

    if (array == null || array[0] == null) {
        return null;
    }

    return array;
}


function checkAuthkey() {
    let authkey = localStorage.getItem('ntdai95_belay_authkey');
    let username = localStorage.getItem('ntdai95_belay_username');
    let paths = window.location.pathname.split('/');
    let pushStateState = {"authkey": authkey, "username": username};

    if (paths.length == 3) {
        pushStateState["channel_id"] = paths[2];
    } else if (paths.length == 5) {
        pushStateState["channel_id"] = paths[2];
        pushStateState["message_id"] = paths[4];
    }

    let pushStateUnused = "";
    let pushStateUrl = "";

    if (authkey === null || authkey === "null") {
        localStorage.setItem("ntdai95_belay_magiclink", document.URL);
        pushStateUnused = "Login/Signup Page";
        pushStateUrl = "http://127.0.0.1:5000";
    } else {
        pushStateUnused = "User Copied Link Page";
        pushStateUrl = document.URL;
    }

    checkState(true, pushStateState, pushStateUnused, pushStateUrl);

    return;
}


function checkState(pushHistory=false, pushStateState=null, pushStateUnused=null, pushStateUrl=null) {
    if (pushHistory) {
        history.pushState(pushStateState, pushStateUnused, pushStateUrl);
    }
    
    if (window.location.pathname.includes('/thread/')) {
        document.querySelector('.auth').style.display = 'none';
        document.querySelector('.channelColumn').style.display = 'block';
        document.querySelector('.messageThreadColumn').style.display = 'block';
        document.querySelector('.message').style.display = 'none';
        document.querySelector('.thread').style.display = 'block';
        startChannelPolling();
        startReplyPolling();
    } else if (window.location.pathname.startsWith('/channel/')) {
        document.querySelector('.auth').style.display = 'none';
        document.querySelector('.channelColumn').style.display = 'block';
        document.querySelector('.messageThreadColumn').style.display = 'block';
        document.querySelector('.message').style.display = 'block';
        document.querySelector('.thread').style.display = 'none';
        startChannelPolling();
        startMessagePolling();
    } else if (window.location.pathname.startsWith('/channel')) {
        document.querySelector('.auth').style.display = 'none';
        document.querySelector('.channelColumn').style.display = 'block';
        document.querySelector('.messageThreadColumn').style.display = 'none';
        startChannelPolling();
    } else {
        document.querySelector('.auth').style.display = 'grid';
        document.querySelector('.channelColumn').style.display = 'none';
        document.querySelector('.messageThreadColumn').style.display = 'none';
    }

    return;
}


window.addEventListener("popstate", () => {checkState();});
