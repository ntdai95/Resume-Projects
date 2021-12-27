import sqlite3


class Database:
    """Database class
    Handles all database actions.
    """
    def __init__(self, name):
        self.__conn = sqlite3.connect(f"{name}.db")
        self.__create_tables(self.__conn)

    ########################
    #   Internal methods   #
    ########################

    def __create_tables(self, connection):
        """Create tables
        Creates all tables using the provided connection.
        Args:
            connection: the database connection
        """
        cursor = connection.cursor()
        with connection:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    email TEXT
                    )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    filename TEXT PRIMARY KEY,
                    username TEXT,
                    tag TEXT,
                    created DATETIME,
                    FOREIGN KEY(username) REFERENCES users(username)
                    )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    topic TEXT PRIMARY KEY,
                    username TEXT,
                    created DATETIME,
                    FOREIGN KEY(username) REFERENCES users(username)
                    )""")

    ########################
    #     User methods     #
    ########################

    def get_user_email(self, username):
        """Get user's email address by username
        Retrieve the user's email address to send out email message.
        Args:
            username: the user id they are registered with
        Returns:
            Success result: boolean whether the username exist in the
            database
            Email: the email address associated with the input username
            found in the database, otherwise returns nothing
            Error/Success message: error message if the username is not
            found in the database, otherwise returns a success message.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM users
                  WHERE username = ?
                  """
            values = (username,)
            result = cursor.execute(sql, values).fetchone()
        if result:
            return True, result[2], "Email sent to user!"
        else:
            return False, None, "No such user found in the database."

    def login(self, username, password):
        """Login
        Allows a user to login to the system.
        Args:
            username: the user id they are registered with
            password: the user's password as a hash
        Returns:
            Success result: boolean whether the username and password
            combination exist in the database
            Error/Success message: error message if the username and
            password combination does not match with the one registered
            in the database, otherwise returns nothing.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT username, password
                  FROM users
                  WHERE
                  username = ?
                  AND password = ?
                  """
            values = (username, password)
            user = cursor.execute(sql, values).fetchone()
            if user:
                return True, None
            else:
                return False, "Invalid username or password! Please, " \
                              "provide the correct username or password!"

    def register(self, username, password, email):
        """Register
        Register a new user of the system including username and password.
        Args:
            username: the user's name
            password: the password for this account
            email: the user's email
        Returns:
            Success result: boolean whether username and password has
            been successfully registered
            Error/Success message: error message if username or email
            already exists, otherwise returns confirmation message.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM users
                  WHERE username = ?
                  """
            values = (username,)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return False, "Username has been used! Please, " \
                              "provide a unique username!"

            sql = """
                  SELECT *
                  FROM users
                  WHERE email = ?
                  """
            values = (email,)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return False, "Email address has been used! Please, " \
                              "provide a unique email address!"

            sql = """
                  INSERT INTO users (username, password, email)
                  VALUES (?, ?, ?)
                  """
            values = (username, password, email)
            cursor.execute(sql, values)
            return True, "Account information sent to email address!"

    def update_password_email(self, email, new_password):
        """Update password by email address
        Updates the user password from old to new.
        Args:
            email: the user's email
            new_password: the new password the user will use
        Returns:
            Success result: boolean whether the email address exists
            in the database
            Error/Success message: error message if the email address
            does not exist, otherwise returns confirmation message.
            Username: if there is an existing user with the requested
            email address in the database
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM users
                  WHERE email = ?
                  """
            values = (email,)
            result = cursor.execute(sql, values).fetchone()
            if result is None:
                return False, "Email address has not been found. Please, " \
                              "enter your registered email address!", None

            username = result[0]
            sql = """
                  UPDATE users
                  SET password = ?
                  WHERE email = ?
                  """
            values = (new_password, email)
            cursor.execute(sql, values)
            return True, "New account information sent to your " \
                         "email address!", username

    def update_password_username(self, username, new_password):
        """Update password by username
        Updates the user password from old to new.
        Args:
            username: the user's username
            new_password: the new password the user will use
        Returns:
            Success result: True, since username must exist at this
            point because the user has already logged in
            Success message: Confirmation message. It is able to update
            the new password because user definitely exists.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  UPDATE users
                  SET password = ?
                  WHERE username = ?
                  """
            values = (new_password, username)
            cursor.execute(sql, values)
            return True, "Password has changed!"

    ########################
    #     Note methods     #
    ########################

    def get_all_notes(self):
        """Get all notes
        Retreive all of the notes in the system.
        Returns:
            Success result: True, even if there is no note in the database
            Note list: a list of all note rows with readable created
            datetime values
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM notes
                  ORDER BY filename ASC
                  """
            notes = cursor.execute(sql).fetchall()
            return True, notes

    def add_note(self, filename, username, tag, created):
        """Add a new note
        Adds a new note to the system.
        Args:
            username: the username of the user who uploads the file
            filename: the name of the note file
            tag: the user selected tag associated with the file
            created: the date when the note was added to the database
        Returns:
            Success result: boolean whether the filename is already
            exist in the database
            Error/Success message: error message if the filename address
            exists, otherwise returns confirmation message.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM notes
                  WHERE filename = ?
                  """
            values = (filename,)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return False, "Please, select a unique filename for your note!"

            sql = """
                  INSERT INTO notes (filename, username, tag, created)
                  VALUES (?, ?, ?, ?)
                  """
            values = (filename, username, tag, created)
            cursor.execute(sql, values)
            return True, "Your note has been uploaded!"

    ########################
    #    Request methods   #
    ########################

    def get_all_requests(self):
        """Get all current requests
        Retrieve all available requests in the system.
        Returns:
            Success result: True, even if there is no request in the database
            Request list: a list of all request rows with readable created
            datetime values
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM requests
                  ORDER BY topic ASC
                  """
            requests = cursor.execute(sql).fetchall()
            return True, requests

    def add_request(self, topic, username, created):
        """Add a new request
        Adds a new request to the system.
        Args:
            topic: the topic of the request
            username: the username of the user who adds the request
            created: the date when the request was added to the database
        Returns:
            Success result: boolean whether the request is already
            exist in the database
            Error/Success message: error message if the request address
            exists, otherwise returns confirmation message.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            sql = """
                  SELECT *
                  FROM requests
                  WHERE topic = ?
                  """
            values = (topic,)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return False, "Request topic has been used! Please, " \
                              "provide a unique request topic!"

            sql = """
                  INSERT INTO requests (topic, username, created)
                  VALUES (?, ?, ?)
                  """
            values = (topic, username, created)
            cursor.execute(sql, values)
            return True, "Request has been added!"

    def delete_request(self, topic, username):
        """Delete an existing request
        Adds an existing request from the system.
        Args:
            topic: the topic of the request
            username: the username of the user who added the request or
            internal for old request deletions
        Returns:
            Success result: boolean whether the request is already
            exist in the database
            Error/Success message: error message if the request address
            does not exists or the user did not created the deleting
            request, otherwise returns confirmation message.
        """
        cursor = self.__conn.cursor()
        with self.__conn:
            if username != "internal":
                sql = """
                    SELECT *
                    FROM requests
                    WHERE topic = ? AND username = ?
                    """
                values = (topic, username)
                result = cursor.execute(sql, values).fetchone()
                if not result:
                    return False, "Request topic does not exist or " \
                                  "you have not created this request! " \
                                  "Therefore, request deletion was unsuccessful!"
            sql = """
                  DELETE FROM requests
                  WHERE topic = ?
                  """
            value = (topic,)
            cursor.execute(sql, value).fetchone()
            return True, "Request has been deleted!"
