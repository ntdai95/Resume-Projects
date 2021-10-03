import os
from database import Database


# to remove previous testing database
if os.path.exists("tests/testing.db"):
    os.remove("tests/testing.db")

# To run : pytest test_database.py
db = Database("tests/testing")


def test_add_user():
    user_id = db.add_user("Min", "client")
    cursor = db.conn.cursor()
    users_table = cursor.execute("SELECT id, name FROM users").fetchall()
    for row in users_table:
        assert row == (user_id, "Min")


def test_add_reservations():
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33"
    customer_id = 1
    datetime_list = ["2021-01-01"]
    to_reserve = "harvest"
    db.add_reservations(reservation_id, customer_id, datetime_list, to_reserve)
    cursor = db.conn.cursor()
    reserv_table = cursor.execute("SELECT * FROM reservations").fetchall()
    for row in reserv_table:
        assert row == (reservation_id, customer_id, datetime_list[0], to_reserve, 0, 0, None)


def test_add_transaction():
    customer_id = 1
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0d125"
    transaction_type = "Reserve"
    cost = 125.0
    down_payment = 110.0
    start_datetime = "2021-01-01"
    db.add_transaction(customer_id, reservation_id, transaction_type, cost, down_payment, start_datetime)
    cursor = db.conn.cursor()
    trans_table = cursor.execute("SELECT * FROM transactions").fetchall()
    for row in trans_table:
        assert row == (1, customer_id, reservation_id, transaction_type, cost, down_payment, start_datetime)


def test_delete_reservation():
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33"
    db.delete_reservation(reservation_id)
    cursor = db.conn.cursor()
    reserv_table = cursor.execute("SELECT * FROM reservations").fetchall()
    assert reserv_table == []


def test_get_transactions():
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0d125"
    result = db.get_transaction(reservation_id)
    assert result == [(1, 1, 125, '2021-01-01')]


def test_get_all_transactions():
    start_date = "2020-12-31"
    end_date = "2021-01-02"
    result = db.get_all_transactions(start_date, end_date)
    assert result == [(1, 1, "c2e10f2a-6604-4c8e-9e2c-9e0c31b0d125", "Reserve", 125, 110, "2021-01-01")]


def test_get_reservations():
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33"
    customer_id = 1
    datetime_list = ["2021-01-01"]
    to_reserve = "harvest"
    db.add_reservations(reservation_id, customer_id, datetime_list, to_reserve)

    start_date = "2020-12-31"
    end_date = "2021-01-02"
    result = db.get_reservations(start_date, end_date)
    assert result == [(reservation_id, customer_id, datetime_list[0], to_reserve, 0, 0, None)]


def test_get_reservations_with_user():
    start_date = "2020-12-31"
    end_date = "2021-01-02"
    result = db.get_reservations(start_date, end_date, 1)
    assert result == [("c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33", 1, "2021-01-01", "harvest", 0, 0, None)]


def test_get_reservations_given_list():
    datetime_list = ["2021-01-01"]
    item_to_reserve = "harvest"
    result = db.get_reservations_given_list(datetime_list, item_to_reserve)
    assert result == [('c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33', 1, 0)]


def test_register():
    name = "aaa"
    email = "aaa@gmail.com"
    user_id = "bbb"
    user_pw = "ccc"
    _type = "client"
    _id = db.register(name, email, user_id, user_pw, _type)
    cursor = db.conn.cursor()
    user = cursor.execute("SELECT name, user_id, user_pw, type, active FROM users WHERE user_id = ?", (user_id,)).fetchone()
    assert user == (name, user_id, user_pw, _type, 1)


def test_login():
    id = "bbb"
    pw = "ccc"
    _type = "client"
    answer = (2, 'bbb', 'ccc', 'client', 1)
    result = db.login(id, pw, _type)
    assert answer == result


def test_set_client_activeness():
    user_id = "bbb"
    active = 0
    _id = db.set_client_activeness(user_id=user_id, active=active)
    cursor = db.conn.cursor()
    user = cursor.execute("SELECT user_id, active FROM users WHERE user_id = ?", (user_id,)).fetchone()
    assert user == (user_id, active)

# test added : save report 
def test_add_report_history():
    id = 1
    search_id = 1
    search_start = "2021-01-01"
    search_end = "2021-12-31"
    search_type = "reservation"
    db.add_report_history(id, search_id, search_start, search_end, search_type)

    cursor = db.conn.cursor()
    info = cursor.execute("SELECT id, search_id, search_start, search_end, search_type FROM history WHERE id = ?", (id,)).fetchall()
    assert len(info) == 1


def test_get_report_history():
    id = 1
    search_type = "reservation"
    result = db.get_report_history(id, search_type)
    assert result == [('1', "2021-01-01", "2021-12-31")]