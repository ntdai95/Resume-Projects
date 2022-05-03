from sqlite3 import connect
from os import path
from json import loads
from uuid import uuid4
from flask import Flask, request, jsonify
from bcrypt import checkpw, hashpw, gensalt


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# --------------------------------- DATABASE -----------------------------------


class Database:
    def __init__(self, db_name):
        self.db_name = db_name


    def create_user(self, username, hashed_password):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE username = '{username}';"
            cursor.execute(sql_query)
            used_user = cursor.fetchone()
            if used_user:
                return {'success': False}

            sql_query = f"SELECT * FROM user;"
            cursor.execute(sql_query)
            all_users = cursor.fetchall()
            used_authkeys = []
            for user in all_users:
                used_authkeys.append(user[1])

            while True:
                authkey = str(uuid4())
                if authkey not in used_authkeys:
                    break

            sql_query = f'INSERT INTO user (authkey, username, hashed_password) VALUES (?, ?, ?);'
            cursor.execute(sql_query, (authkey, username, hashed_password))
            connection.commit()
            return {'success': True, "authkey": authkey}


    def check_user(self, username, password):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE username = '{username}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            if checkpw(password, user[3]):
                return {'success': True, "authkey": user[1]}

            return {'success': False}


    def create_channel(self, authkey, channelName):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f'INSERT INTO channel (name) VALUES (?);'
            cursor.execute(sql_query, (channelName,))
            connection.commit()
            return {'success': True}


    def get_all_channels(self, authkey):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = "SELECT * FROM channel;"
            cursor.execute(sql_query)
            channels = cursor.fetchall()
            return {'success': True, 'channels': channels}


    def create_message(self, authkey, newMessage, username, channel_id):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f'INSERT INTO message (content, username, channel_id, is_reply, replies_to) VALUES (?, ?, ?, ?, ?);'
            cursor.execute(sql_query, (newMessage, username, channel_id, False, None))
            connection.commit()
            return {'success': True}


    def get_all_messages(self, authkey, channel_id):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f"SELECT * FROM message WHERE channel_id = '{channel_id}' AND is_reply = 0;"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            messages = []
            for message in result:
                sql_query = f"SELECT * FROM message WHERE is_reply = 1 AND replies_to = '{message[0]}';"
                cursor.execute(sql_query)
                result = cursor.fetchall()
                number_of_replies = len(result)
                messages.append([message[0], message[1], message[2], number_of_replies, message[3]])

            return {'success': True, 'messages': messages}


    def create_reply(self, authkey, newReply, username, channel_id, message_id):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f'INSERT INTO message (content, username, channel_id, is_reply, replies_to) VALUES (?, ?, ?, ?, ?);'
            cursor.execute(sql_query, (newReply, username, channel_id, True, message_id))
            connection.commit()
            return {'success': True}


    def get_all_replies(self, authkey, channel_id, message_id):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f"SELECT * FROM message WHERE message_id = '{message_id}';"
            cursor.execute(sql_query)
            message = cursor.fetchone()

            sql_query = f"SELECT * FROM message WHERE channel_id = '{channel_id}' AND is_reply = 1 AND replies_to = '{message_id}';"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            replies = []
            for reply in result:
                replies.append([reply[0], reply[1], reply[2]])

            return {'success': True, 'message': message, 'replies': replies}


    def update_last_seen_message(self, authkey, username, channel_id, message_id):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f"SELECT * FROM user_channel WHERE username = '{username}' AND channel_id = '{channel_id}' AND latest_seen_message_id = '{message_id}';"
            cursor.execute(sql_query)
            user_channel = cursor.fetchone()
            if not user_channel:
                sql_query = f'INSERT INTO user_channel (username, channel_id, latest_seen_message_id) VALUES (?, ?, ?);'
                cursor.execute(sql_query, (username, channel_id, message_id))
            else:
                sql_query = f"UPDATE user_channel SET latest_seen_message_id = '{message_id}' WHERE username = '{username}' AND channel_id = '{channel_id}';"
                cursor.execute(sql_query)

            connection.commit()
            return {'success': True}


    def get_all_unread_message_counts(self, authkey, username):
        connection = connect(path.join(path.join(path.dirname(__file__), "database"), f"{self.db_name}.db"), check_same_thread=False)
        cursor = connection.cursor()
        with connection:
            sql_query = f"SELECT * FROM user WHERE authkey = '{authkey}';"
            cursor.execute(sql_query)
            user = cursor.fetchone()
            if not user:
                return {'success': False}

            sql_query = f"SELECT * FROM channel ORDER BY channel_id ASC;"
            cursor.execute(sql_query)
            channels = cursor.fetchall()
            if channels == []:
                return {'success': True, 'channel_idCounts': []}

            channel_idCounts = []
            for channel in channels:
                sql_query = f"SELECT * FROM user_channel WHERE username = '{username}' AND channel_id = '{channel[0]}';"
                cursor.execute(sql_query)
                user_channel = cursor.fetchone()
                if not user_channel:
                    sql_query = f"SELECT * FROM message WHERE channel_id = '{channel[0]}' AND is_reply = 0;"
                else:
                    sql_query = f"SELECT * FROM message WHERE message_id > '{user_channel[2]}' AND channel_id = '{channel[0]}' AND is_reply = 0;"

                cursor.execute(sql_query)
                new_messages = cursor.fetchall()
                channel_idCounts.append(tuple([channel[0], len(new_messages)]))

            return {'success': True, 'channel_idCounts': channel_idCounts}


DB = Database("belay")


# -------------------------------- HTML PATHS -----------------------------------


@app.route('/')
@app.route('/channel')
@app.route('/channel/<int:channel_id>')
@app.route('/channel/<int:channel_id>/thread/<int:thread_id>')
def index(channel_id=None, thread_id=None):
    return app.send_static_file('index.html')


# -------------------------------- API ROUTES ----------------------------------


@app.route('/api/user', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password').encode('utf-8')

        result = DB.check_user(username, password)
        return jsonify(result)
    elif request.method == 'POST':
        username = loads(request.data)['username']
        password = loads(request.data)['password'].encode('utf-8')
        hashed_password = hashpw(password, gensalt())

        result = DB.create_user(username, hashed_password)
        return jsonify(result)


@app.route('/api/channel', methods=['GET', 'POST'])
def channel():
    if "Authorization" not in list(request.headers.keys()):
        return jsonify({"success": False})
    else:
        authkey = request.headers["Authorization"]

    if request.method == 'GET':
        result = DB.get_all_channels(authkey)
        return jsonify(result)
    elif request.method == 'POST':
        channelName = loads(request.data)['channelName']

        result = DB.create_channel(authkey, channelName)
        return jsonify(result)


@app.route('/api/channel/<int:channel_id>/message', methods=['GET', 'POST'])
def message(channel_id):
    if "Authorization" not in list(request.headers.keys()):
        return jsonify({"success": False})
    else:
        authkey = request.headers["Authorization"]

    if request.method == 'GET':
        result = DB.get_all_messages(authkey, channel_id)
        return jsonify(result)
    elif request.method == 'POST':
        newMessage = loads(request.data)['newMessage']
        username = loads(request.data)['username']

        result = DB.create_message(authkey, newMessage, username, channel_id)
        return jsonify(result)


@app.route('/api/channel/<int:channel_id>/message/<int:message_id>', methods=['GET', 'POST'])
def reply(channel_id, message_id):
    if "Authorization" not in list(request.headers.keys()):
        return jsonify({"success": False})
    else:
        authkey = request.headers["Authorization"]

    if request.method == 'GET':
        result = DB.get_all_replies(authkey, channel_id, message_id)
        return jsonify(result)
    elif request.method == 'POST':
        newReply = loads(request.data)['newReply']
        username = loads(request.data)['username']

        result = DB.create_reply(authkey, newReply, username, channel_id, message_id)
        return jsonify(result)


@app.route('/api/message/unread', methods=['GET', 'POST'])
def unread_message_counts():
    if "Authorization" not in list(request.headers.keys()):
        return jsonify({"success": False})
    else:
        authkey = request.headers["Authorization"]

    if request.method == 'GET':
        username = request.args.get('username')

        result = DB.get_all_unread_message_counts(authkey, username)
        return jsonify(result)
    elif request.method == 'POST':
        username = loads(request.data)['username']
        channel_id = loads(request.data)['channel_id']
        message_id = loads(request.data)['message_id']

        result = DB.update_last_seen_message(authkey, username, channel_id, message_id)
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
