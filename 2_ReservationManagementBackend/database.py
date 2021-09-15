from datetime import datetime
from pydantic.types import Json
from sqlite3 import Connection
from typing import Any, List, Optional
import sqlite3


class Database:
    """Database class

    Handles all database actions.
    """
    def __init__(self, name: str):
        self.name = name
        self.conn = sqlite3.connect(name)
        self.create_tables(self.conn)

    #######################
    #   Internal methods  #
    #######################

    def create_tables(self, connection: Connection, drop: bool = False) -> None:
        """Create tables

        Creates all tables using the provided connection. Also allows a drop of tables.

        Args:
            connection: the database connection
            drop: true if we should drop all tables and recreate
        """
        cursor = connection.cursor()
        with connection:
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    user_id TEXT,
                    user_pw TEXT,
                    type TEXT,
                    active INTEGER DEFAULT 1,
                    funds REAL,
                    email TEXT
                    )""")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER,
                    customer_id INTEGER,
                    reservation_datetime DATETIME,
                    item_to_reserve TEXT,
                    cancelled INTEGER DEFAULT 0,
                    on_hold INTEGER DEFAULT 0,
                    held_for_user TEXT,
                    FOREIGN KEY(customer_id) REFERENCES users(id)
                    )
                """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    reservation_id INTEGER,
                    transaction_type TEXT,
                    cost INTEGER,
                    down_payment INTEGER,
                    transaction_datetime DATETIME,
                    FOREIGN KEY(customer_id) REFERENCES users(id)
                    FOREIGN KEY(reservation_id) REFERENCES reservations(id)
                    )
                """)
            cursor.execute("""CREATE TABLE IF NOT EXISTS history (
                        id INTEGER,
                        search_id TEXT,
                        search_start DATETIME,
                        search_end DATETIME,
                        search_type TEXT
                        )
                    """)

    def check_db(self) -> None:
        """Check db

        Method to check database tables. Prints the main tables into logs.
        """
        print('\n--------- Displaying DB Check Below ---------')
        cursor = self.conn.cursor()
        with self.conn:
            users_table = cursor.execute("SELECT * FROM users").fetchall()
            transactions_table = cursor.execute("SELECT * FROM transactions").fetchall()
            reservations_table = cursor.execute("SELECT * FROM reservations").fetchall()
        print("\nUsers table below:")
        for row in users_table:
            print(row)
        print("\nTransactions table below:")
        for row in transactions_table:
            print(row)
        print("\nReservations table below:")
        for row in reservations_table:
            print(row)
        print('--------- End DB Check Below ---------\n')

    #######################
    #     User methods    #
    #######################

    def add_user(self, name: str, user_type: str) -> int:
        """Add a new user

        Adds a new user to the database included their user type and associated starting values.

        Args:
            name: customer or user name
            user_type: client or manager
        Returns:
            user_id: the id associated with the newly created user
        """
        allowed_types = ['client', 'manager']
        if user_type not in allowed_types:
            print(f"User type not allowed, no user created")
            return 
        else:
            cursor = self.conn.cursor()
            balance = 10000
            with self.conn:
                sql = "INSERT INTO users (id, name, user_id, type, funds) VALUES (?, ?, ?, ?, ?)"
                values = (None, name, name, user_type, 10000)
                cursor.execute(sql, values)
                customer_id = cursor.lastrowid
            print(f"{user_type} inserted, id = {customer_id}, account balance = {balance}")
            return customer_id

    def register(self, name: str, email: str, user_id: str, user_pw: str, _type: str) -> int:
        """Register

        Register a new user of the system including their id and password.

        Args:
            name: the user's name
            email: the user's email
            user_id: the requested login id
            user_pw: the password for this account
            _type: client or manager
        Returns:
            customer_id: the assigned user_id for this account
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT id, user_id, user_pw FROM users WHERE user_id = ? AND type = ?"
            values = (user_id, _type)
            result = cursor.execute(sql, values).fetchone()
            if result:
                print("Already in use id")
                return None
            sql = "INSERT INTO users (id, name, user_id, user_pw, type, active, funds, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            values = (None, name, user_id, user_pw, _type, 1, 1000, email)
            cursor.execute(sql, values)
            customer_id = cursor.lastrowid
        print(f"User inserted, customer id = {customer_id}.")
        return customer_id

    def login(self, id: str, pw: str, _type: str) -> Json:
        """Login

        Allows a user to login to the system.

        Args: 
            id: the user id they are registered with
            pw: the user's password as a hash
            _type: manager or client
        Returns:
            a json row of id, user_id, user_pw, type, active
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                  SELECT id, user_id, user_pw, type, active
                  FROM users
                  WHERE
                  user_id = ? 
                  AND user_pw = ? 
                  AND type = ?
                  """
            values = (id, pw, _type)
            result = cursor.execute(sql, values).fetchone()
            return result

    def set_client_activeness(self, user_id: int, active: int) -> Optional[int]:
        """Set client activeness

        Set whether a client account is enabled or disabled

        Args:
            user_id: the user's id to change
            active: the new value of active
        Returns:
            None or user_id if successful
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = "SELECT id FROM users WHERE user_id = ?"
            values = (user_id,)
            result = cursor.execute(sql, values).fetchone()
            if result is None:
                return None
            sql = """
                UPDATE users 
                SET active = ?
                WHERE user_id = ?
                """
            values = (active, user_id)
            cursor.execute(sql, values)
            return user_id

    def update_password(self, user_id: str, new_pw: str) -> Optional[str]:
        """Update password

        Updates the user password from old to new.

        Args:
            user_id: the user's login id
            new_pw: the new password the user will use
        Returns:
            user_id if there was an error
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT user_pw
                FROM users
                WHERE id = ?"""
            values = (user_id,)
            password_hash = cursor.execute(sql, values).fetchone()
            sql = """
                UPDATE users
                SET user_pw = ?
                WHERE id = ?"""
            values = (new_pw, user_id)
            cursor.execute(sql, values)
            sql = """
                SELECT user_pw
                FROM users
                WHERE id = ?"""
            values = (user_id,)
            new_password_hash = cursor.execute(sql, values).fetchone()
        if new_password_hash != password_hash:
            return user_id

    def get_user(self, user_id: str) -> List[Json]:
        """Get a user

        Retrieve a user row.

        Args:
            user_id: the id of the user to retrieve
        Returns:
            a user row
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT * from users
                WHERE id = ?"""
            values = (user_id,)
            user = cursor.execute(sql, values).fetchall()
        return user

    def get_user_without_session(self, email: str) -> List[Json]:
        """Get a user

        Retrieve a user row.

        Args:
            email: the email of the user to retrieve
        Returns:
            a user row
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT * from users
                WHERE email = ?"""
            values = (email,)
            user = cursor.execute(sql, values).fetchall()
        return user

    def get_clients(self) -> List[Json]:
        """Get all clients

        Retreive all of the clients in the system.

        Returns:
            a list of all user rows
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT name, user_id, active, funds from users
                WHERE type = ?"""
            values = ("client",)
            user = cursor.execute(sql, values).fetchall()
        return user
    
    def find_exact_client(self, pname: str) -> List[Json]:
        """Get the exact client by name

        Find an exact client match.

        Args:
            pname: the name of the client
        Returns:
            the user row 
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT id, name, user_id FROM users
                WHERE type = ? AND name = ?"""
            values = ("client", pname)
            user = cursor.execute(sql, values).fetchall()
        return user

    def find_client(self, pname: str) -> List[Json]:
        """Find clients

        Do a search with a partial name for clients.

        Args:
            pname: the partial name of the client (starts with)
        Returns:
            a list of potential matches
        """
        cursor = self.conn.cursor()
        with self.conn:
            query ="SELECT id, name, user_id FROM users WHERE type='client' AND name LIKE '" + pname +"%'"
            user = cursor.execute(query).fetchall()
        return user

    def get_user_funds(self, user_id: str) -> float:
        """Get user funds
        
        Get funds for a client account.

        Args:
            user_id: the user_id of the account to check funds in
        Returns:
            the amount of funds or 0
        """
        cursor = self.conn.cursor()
        user_funds = cursor.execute("SELECT funds from users WHERE id = ?", (user_id,)).fetchone()[0]
        if not user_funds:
            return 0
        else:
            return float(user_funds)

    def post_user_funds(self, user_id: str, amount: str) -> float:
        """Post user funds
        
        Add funds to a client account.

        Args:
            user_id: the user_id of the client to add funds to
            amount: the amount of funds to add as a string
        """
        cursor = self.conn.cursor()
        user_funds = self.get_user_funds(user_id) + float(amount)
        if user_funds < 0:
            print("user_funds < 0. Value would be: ", user_funds)
            return False
        with self.conn:
            sql = """
                UPDATE users
                SET funds = ?
                WHERE id = ?"""
            values = (user_funds, user_id)
            cursor.execute(sql, values)
        return user_funds

    #######################
    # Reservation methods #
    #######################

    def add_reservations(self,
            reservation_id: str,
            customer_id: str,
            datetime_list: List[datetime],
            to_reserve: str) -> None:
        """Add a new reservation

        Adds a new reservation to the system.

        Args:
            reservation_id: the uuid of the reservation
            customer_id: the customer reserving it
            datetime_list: the list of all relevant datetime blocks
            to_reserve: the item to reserve
        """
        cursor = self.conn.cursor()
        reservation_id_list = []
        with self.conn:
            sql = """
                INSERT INTO reservations
                (id,
                customer_id,
                reservation_datetime,
                item_to_reserve)
                VALUES (?, ?, ?, ?)"""
            for date in datetime_list:
                values = (reservation_id,
                          customer_id,
                          date,
                          to_reserve)
                cursor.execute(sql, values)
                reservation_id_list.append(cursor.lastrowid)
        print(f"Reservation ids added: {reservation_id_list}.")

    def add_holds(self,
            reservation_id: str,
            customer_id: str,
            datetime_list: List[datetime],
            to_reserve: str,
            held_for_user: str) -> None:
        """Add a new reservation hold

        Adds a new hold for an external client.

        Args:
            reservation_id: the uuid of the reservation
            customer_id: the person making a hold
            datetime_list: the list of all relevant datetime blocks
            to_reserve: the item to reserve
            held_for_user: the customer it is held for
        """
        cursor = self.conn.cursor()
        hold_id_list = []
        with self.conn:
            sql = """
                INSERT INTO reservations
                (id,
                customer_id,
                reservation_datetime,
                item_to_reserve, 
                on_hold, 
                held_for_user)
                VALUES (?, ?, ?, ?, ?, ?)"""
            for date in datetime_list:
                values = (reservation_id,
                          customer_id,
                          date,
                          to_reserve, 
                          1,
                          held_for_user)
                cursor.execute(sql, values)
                hold_id_list.append(cursor.lastrowid)
        print(f"Hold reservation ids added: {hold_id_list}.")

    def add_hold_status_to_reservation(self, client_name: str, reservation_id: str) -> None:
        """Add hold status to reservation

        Updating a reservation to a hold status.

        Args:
            reservation_id: the uuid for the reservation to change to hold
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                UPDATE reservations
                SET on_hold = ?, held_for_user = ?
                WHERE id = ?"""
            values = (1, client_name, reservation_id)
            cursor.execute(sql, values)
        print(f"Reservation id on hold: {reservation_id}")

    def get_reservation_by_id(self, reservation_id: str) -> List[Json]:
        """Get reservation by id

        Get a single reservation using the reservation id.

        Args:
            reservation_id: the uuid for the reservation
        Returns:
            list of reservation rows
        """
        cursor = self.conn.cursor()
        reservation_list = []
        sql = """
            SELECT * 
            FROM reservations
            WHERE 
            id = ?
            """
        values = (reservation_id,)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        for x in result:
            reservation_list.append(x)
        return reservation_list

    def get_single_reservation(self, reservation_id: str) -> List[Json]:
        """Get a reservation based on reservation_id

        Duplicative funciton to get_reservation_by_id but different execution.
        """
        reservation_list = []
        cursor = self.conn.cursor()
        sql = """
            SELECT * 
            FROM reservations
            WHERE id = ?
            """
        values = (reservation_id,)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        for x in result:
            reservation_list.append(x)
        print("GET SINGLE RES: ", reservation_list)
        return reservation_list

    def edit_reservation(self, 
            reservation_id: str, 
            field_to_edit: str, 
            new_value: str) -> List[Json]:
        """Edit reservation

        Edit a reservation based on reservation_id.

        Args:
            reservation_id: uuid for reservation
            field_to_edit: the field to change
            new_value: the value to put there
        Returns:
            false or the rows changed
        """
        reservation_list = []
        allowed_columns = ['reservation_datetime', 'item_to_reserve', 'cancelled']
        curr_reservation_list = self.get_single_reservation(reservation_id)
        if len(curr_reservation_list) == 0:
            return False
        elif field_to_edit not in allowed_columns:
            return False
        else:
            cursor = self.conn.cursor()
            sql = """
                UPDATE reservations
                SET ? = ?
                WHERE id = ?"""
            values = (field_to_edit, new_value, reservation_id)
            with self.conn:
                result = cursor.execute(sql, values).fetchall()
            for x in result:
                reservation_list.append(x)
            print("EDIT RES: ", reservation_list)
            return reservation_list

    def get_hold_reservations(self):
        """Get hold reservations

        Get the reservations which are holds.

        Returns:
            list of rows for holds
        """
        cursor = self.conn.cursor()
        reservation_list = []
        sql = """
            SELECT * 
            FROM reservations
            WHERE 
            on_hold = ?
            """
        values = (1,)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        for x in result:
            reservation_list.append(x)
        return reservation_list

    def get_reservations(self,
            start_date: datetime,
            end_date: datetime,
            customer_id: int = 0) -> List[Any]:
        """Get reservations

        Get reservation with customer id and start/end time.

        Args:
            start_date: the starting date to pull from
            end_date: the ending inclusive date to pull to
            customer_id: the customer id for reservations
        Returns:
            list of rows which are the reservations that match
        """
        cursor = self.conn.cursor()
        reservation_list = []
        start_datetime = datetime.strptime(start_date + " " + "00:00", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_date + " " + "23:59", "%Y-%m-%d %H:%M")
        if customer_id > 0:
            sql = """
                SELECT * 
                FROM reservations
                WHERE 
                (reservation_datetime BETWEEN ? and ?)
                AND (customer_id = ?)
                """
            values = (start_datetime, end_datetime, customer_id)
        else:
            sql = """
                SELECT * 
                FROM reservations
                WHERE 
                (reservation_datetime BETWEEN ? and ?)
                """
            values = (start_datetime, end_datetime)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        for x in result:
            reservation_list.append(x)
        return reservation_list

    def get_reservations_given_list(self,
            datetime_list: List[datetime],
            item_to_reserve: str) -> List[Any]:
        """Get reservations given list
        
        Get reservations with date list that is provided rather than id or criteria. Used by
        by specific functions to make a single search instead of many.

        Args:
            datetime_list: a list of appropriate datetimes to retrieve
            item_to_reserve: the specific item to find reservations on
        Returns:
            a list of the matching rows
        """
        cursor = self.conn.cursor()
        reservation_list = []
        for date in datetime_list:
            sql = """
                SELECT id, customer_id, cancelled 
                FROM reservations
                WHERE
                (reservation_datetime = ?)
                AND 
                item_to_reserve = ?
                """
            values = (date, item_to_reserve)
            with self.conn:
                result = cursor.execute(sql, values).fetchone()
                if result:
                    reservation_list.append(result)
        return reservation_list

    def delete_reservation(self, reservation_id: str) -> None:
        """Delete reservation
        
        Delete a reservation from the database completely.

        Args:
            reservation_id: the uuid of the reservation to delete
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                DELETE FROM reservations
                WHERE 
                id = ?"""
            value = (reservation_id,)
            cursor.execute(sql, value).fetchone()
        print(f"Reservation Deleted: {reservation_id}.")

    #######################
    # Transaction methods #
    #######################

    def add_transaction(self,
            customer_id: str,
            reservation_id: str,
            transaction_type: str,
            cost: float,
            down_payment: float,
            start_datetime: datetime) -> None:
        """Add transaction

        Adds a transaction to the database of transactions.

        Args:
            customer_id: the id of the customer that did the transaction
            reservation_id: the uuid of the reservation 
            transaction_type: the thing that happened
            cost: any dollar amount for this transaction
            down_payment: the down payment amount if reservation related
            start_datetime: only the earliest datetime for this action
        """
        cursor = self.conn.cursor()
        transaction_id_list = []
        down_payment = float("{:.2f}".format(down_payment))
        cost = float("{:.2f}".format(cost))
        with self.conn:
            sql = """
                INSERT INTO transactions
                (id,
                customer_id,
                reservation_id,
                transaction_type,
                cost,
                down_payment,
                transaction_datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
            values = (None,
                      customer_id,
                      reservation_id,
                      transaction_type,
                      cost,
                      down_payment,
                      start_datetime)
            cursor.execute(sql, values)
            transaction_id_list.append(cursor.lastrowid)
        print(f"Transaction ids added: {transaction_id_list}.")

    def get_transaction(self, reservation_id: str) -> Any:
        """Get transaction

        Get a single transaction based on id.

        Args:
            reservation_id: the reservation id for this transaction
        Returns:
            the transaction row
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                SELECT id, customer_id, cost, transaction_datetime
                FROM transactions
                WHERE
                reservation_id = ?
                """
            values = (reservation_id,)
            transaction_data = cursor.execute(sql, values).fetchall()
        return transaction_data

    def get_all_transactions(self, 
            start_date: datetime, 
            end_date: datetime, 
            customer_id: int = None) -> List[Any]:
        """Get all transactions

        Get all transactions with a customer_id and within the daterange.

        Args:
            start_date: starting datetime
            end_date: ending datetime
            customer_id: the customer_id for transaction search
        """
        cursor = self.conn.cursor()
        transaction_list = []
        start_datetime = datetime.strptime(start_date + " " + "00:00", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_date + " " + "23:59", "%Y-%m-%d %H:%M")

        if customer_id:
            sql = """
                SELECT *
                FROM transactions
                WHERE 
                (transaction_datetime BETWEEN ? and ?)
                AND
                (customer_id = ?)
                """
            values = (start_datetime, end_datetime, customer_id)
        else:
            sql = """
                SELECT *
                FROM transactions
                WHERE 
                (transaction_datetime BETWEEN ? and ?)
                """
            values = (start_datetime, end_datetime)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        for x in result:
            transaction_list.append(x)
        return transaction_list

    #######################
    # History methods #
    #######################

    def add_report_history(self, 
            id: str, 
            search_id: int, 
            search_start: datetime, 
            search_end: datetime, 
            search_type: str) -> Json:
        """Add report history

        Adds a report to a user's history so they can pull it again.

        Args:
            id: the user id
            search_id: the saved search id
            search_start: the datetime for the search
            search_end: datetime for end of search
            search_type: the type of search conducted
        Returns:
            json with saved row info
        """
        cursor = self.conn.cursor()
        with self.conn:
            sql = """
                INSERT INTO history
                (id,
                search_id,
                search_start,
                search_end, 
                search_type)
                VALUES (?, ?, ?, ?, ?)"""
            values = (id,
                      search_id,
                      search_start,
                      search_end,
                      search_type)
            cursor.execute(sql, values)
        print(f"report_history is added: {[id, search_id, search_start, search_end, search_type]}")
        return {"id": id, "search_id": search_id, "search_start": search_start, 
            "search_end": search_end, "search_type": search_type}

    def get_report_history(self, id, search_type):
        """Get report history

        Get the report history given id and search_type.

        Args:
            id: the search id
            search_type: the type of the search
        Returns:
            a list of the matching rows
        """
        cursor = self.conn.cursor()
        sql = """
            SELECT search_id, search_start, search_end 
            FROM history
            WHERE
            id = ? 
            AND
            search_type = ?
            """
        values = (id, search_type)
        with self.conn:
            result = cursor.execute(sql, values).fetchall()
        print(result)
        return result
