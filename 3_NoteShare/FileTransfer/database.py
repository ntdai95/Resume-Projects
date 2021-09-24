import sqlite3


class Database:
    """Database class
    Handles all database actions.
    """
    def __init__(self, name):
        self.conn = sqlite3.connect(f"{name}.db")
        self.create_tables(self.conn)

    ########################
    #   Internal methods   #
    ########################

    def create_tables(self, connection):
        """Create tables
        Creates all tables using the provided connection.
        Args:
            connection: the database connection
        """
        cursor = connection.cursor()
        with connection:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    email TEXT
                    )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT
                    tag TEXT
                    )""")
    
    ########################
    #     User methods     #
    ########################

    def register(self, username, password, email):
        """Register
        Register a new user of the system including username and password.
        Args:
            username: the user's name
            password: the password for this account
            email: the user's email
        Returns:
            customer_id: the assigned user_id for this account
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT username, email FROM users WHERE username = ? OR email = ?"
            values = (username, email)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return None
            sql = "INSERT INTO users (id, username, password, email) VALUES (?, ?, ?, ?)"
            values = (None, username, password, email)
            cursor.execute(sql, values)
            customer_id = cursor.lastrowid
        return customer_id


    def login(self, username, password):
        """Login
        Allows a user to login to the system.
        Args: 
            username: the user id they are registered with
            password: the user's password as a hash
        Returns:
            a boolean whether username with password exists in the database
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                  SELECT id, username, password, email
                  FROM users
                  WHERE
                  username = ? 
                  AND password = ? 
                  """
            values = (username, password)
            user = cursor.execute(sql, values).fetchone()
            if user:
                return False
            return True


    def update_password(self, email, new_password):
        """Update password
        Updates the user password from old to new.
        Args:
            email: the user's email
            new_password: the new password the user will use
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT * FROM users WHERE email = ?"
            values = (email,)
            result = cursor.execute(sql, values).fetchone()
            if result:
                return False
            sql = "UPDATE users SET password = ? WHERE email = ?"
            values = (new_password, email)
            cursor.execute(sql, values)
            return True

    ########################
    #     Note methods     #
    ########################

    def add_note(self, filename, tag):
        """Add a new note
        Adds a new note to the system.
        Args:
            filename: the name of the note file
            author: the username of the user who uploads the file
            tag: the user selected tag associated with the file
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "INSERT INTO notes (id, filename, tag) VALUES (?, ?, ?)"
            values = (None, filename, tag)
            cursor.execute(sql, values)


    def get_all_notes(self):
        """Get all notes
        Retreive all of the notes in the system.
        Returns:
            a list of all notes rows
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT * FROM notes"
            notes = cursor.execute(sql).fetchall()
        return notes

    
    def get_note(self, note_id):
        """Get a specific note
        Retreive the specific note in the system.
        Returns:
            a specific notes row
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT * FROM notes WHERE id = ?"
            values = (note_id,)
            note = cursor.execute(sql, values).fetchone()
        return note