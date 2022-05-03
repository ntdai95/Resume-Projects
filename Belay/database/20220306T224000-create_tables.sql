DROP TABLE IF EXISTS user_channel;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS channel;
DROP TABLE IF EXISTS user;


CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    authkey VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    hashed_password BLOB NOT NULL
);


CREATE TABLE IF NOT EXISTS channel (
    channel_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    content TEXT,
    username VARCHAR(100) NOT NULL,
    channel_id INTEGER NOT NULL,
    is_reply BOOLEAN NOT NULL,
    replies_to INTEGER,
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
);


CREATE TABLE IF NOT EXISTS user_channel (
    username VARCHAR(100) NOT NULL,
    channel_id INTEGER NOT NULL,
    latest_seen_message_id INTEGER NOT NULL,
    FOREIGN KEY (username) REFERENCES user(username),
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id),
    FOREIGN KEY (latest_seen_message_id) REFERENCES message(message_id)
);
