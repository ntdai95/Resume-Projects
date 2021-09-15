# import os
# to remove reservation_system to initialize db 
# if os.path.exists("test_db"):
#    os.remove("test_db")

import json
import pytest
import main
from datetime import datetime
from uuid import uuid4
from fastapi.testclient import TestClient


# Tests for the stages of the system
# Coverage: 93%

# To run : (remove reservation_system file with import os) 


client = TestClient(main.app)
# inject manager session for testing
t_session = str(uuid4())
main.sessions[t_session] = [datetime.today(), 'manager']


def test_load_config():
    assert main.environment == "prod"
    assert main.client_login == main.client_login
    assert main.manager_registration == 1


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "You must use /v1/"}


def test_read_root_v1():
    response = client.get("/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Reservation System Root V1"}


def test_hold_get():
    url = "/hold"
    response = client.get(url)

    assert response.status_code == 200
    assert len(json.loads(response.json())) >= 0


# after: start_time/start_date
# before: end_time/end_date
@pytest.mark.parametrize("data, response", [
    (
            {'username': 'wrong user',
             'password': 'wrong password',
             'client_name': 'dai',
             'request': 'mini microvac1',
             'start_date': '2021-06-24',
             'start_time': '12:00',
             'end_time': '13:00'},
            200
    )
])
def test_hold_post_error(data, response):
    url = "/hold"
    data = {"username": data['username'],
            "password": data['password'],
            "client_name": data['client_name'],
            "request": data['request'],
            "start_date": data['start_date'],
            "start_time": data['start_time'],
            "end_time": data['end_time']}

    result = client.post(url, json=data)

    print(result.json())
    assert result.status_code == response
    assert result.json()['success'] == False
    assert result.json()['message'] == 'Invalid id/password'
    assert result.json()['facility_name'] == 'APIGROUP5 at Chicago, IL'


# after: start_time/start_date
# before: end_time/end_date
@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '1',
             'reservation_date': '2021-09-15',
             'thing_to_reserve': 'workshop1',
             'start_time': '12:30',
             'end_time': '13:30'},
            200
    )
])
def test_post_reservations(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)
    # client.delete(url, params={"reservation_id": result.json()["reservation_id"], "session": t_session})

    total_cost = 99.0
    down_payment = 49.5

    print(result.json())
    assert result.status_code == response
    assert result.json()['total_cost'] == total_cost
    assert result.json()["down_payment"] == down_payment


@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '2',
             'reservation_date': '2022-02-03',
             'thing_to_reserve': 'microv1',
             'start_time': '14:00',
             'end_time': '15:00',
             'session': t_session},
            200
    )
])
def test_post_reservations1(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)
    # client.delete(url, params={"reservation_id": result.json()["reservation_id"], "session": t_session})

    total_cost = 1500.0
    down_payment = 750.0

    assert result.status_code == response
    assert result.json()['total_cost'] == total_cost
    assert result.json()["down_payment"] == down_payment


@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '1',
             'reservation_date': '2022-01-07',
             'thing_to_reserve': 'asdf',
             'start_time': '11:30',
             'end_time': '13:30'},
            200
    )
])
# error handling for machines out of range (microv1-2/irrad1-2/extrud1-2/crusher/harvest)
def test_post_reservations_error(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)

    error_msg = {"message": "That machine does not exist."}

    assert result.status_code == response
    assert result.json() == error_msg


@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '1',
             'reservation_date': '2022-01-07',
             'thing_to_reserve': 'workshop16',
             'start_time': '11:30',
             'end_time': '13:30'},
            200
    )
])
# error handling for workshops out of range (workshop1-15)
def test_post_reservations_exceed_workshop(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)

    error_msg = {'message': 'That workshop does not exist.'}

    assert result.json() == error_msg


@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '1',
             'reservation_date': '2020-01-01',
             'thing_to_reserve': 'workshop1',
             'start_time': '11:30',
             'end_time': '13:30'},
            200
    )
])
# error handling for past date/time reservation
def test_post_reservations_error_past_date(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)

    error_msg = {"message": "This date or time is in the past."}

    assert result.json() == error_msg


@pytest.mark.parametrize("data, response", [
    (
            {'customer_id': '1',
             'reservation_date': '2020.01.01',
             'thing_to_reserve': 'workshop1',
             'start_time': '11:30',
             'end_time': '13:30'},
            200
    )
])
# error handling for wrong data format
def test_post_reservations_error_wrong_date_format(data, response):
    url = "/v1/reservations/"
    params = {"thing_to_reserve": data['thing_to_reserve'],
              "reservation_date": data['reservation_date'],
              "start_time": data['start_time'],
              "end_time": data['end_time'],
              "customer_id": data['customer_id'],
              'session': t_session}

    result = client.post(url, params=params)

    error_msg = {"message": "This is not a valid date or time format. Required:  YYYY/MM/DD"}

    assert result.json() == error_msg


def test_get_reservations1():
    url = "http://localhost:51225/v1/reservations/"
    parameters = {"end": "2021-06-30", "start": "2021-06-01", "customer_id": 1,'session': t_session}
    response = client.get(url, params=parameters)
    print("---get reservation --- ")
    assert json.loads(response.content)["message"] == "We did not find any reservations with those details."
    assert response.status_code == 200


def test_get_reservations2():
    parameters = {"end": "2022-02-27", "start": "2022-01-01", 'session': t_session}
    response = client.get('http://localhost:51225/v1/reservations/', params=parameters)

    print("---get reservation --- ")
    print(response.status_code)
    print(response.json())
    assert len(json.loads(response.json())) == 2
    assert response.status_code == 200


def test_delete_reservation():
    parameters = {"reservation_id": "invalid_id", 'session': t_session}
    response = client.delete('http://localhost:51225/v1/reservations/', params=parameters)

    assert response.status_code == 200
    assert json.loads(response.content)["message"] == "This reservation does not exist or was already canceled."


def test_get_transactions():
    parameters = {"end": '2022-03-30', "start": '2021-06-01', 'session': t_session}
    response = client.get('http://localhost:51225/v1/transactions/',
                          params=parameters)
    print("---get transactions --- ")
    print(response.content)
    assert len(json.loads(response.json())) == 2
    assert response.status_code == 200


def test_reset_prod():
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c"
    response = client.get("http://localhost:51225/v1/reset_app/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == {"message": "Method not allowed in production."}


def test_reset_dev():
    main.environment = "dev"
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c"
    answer = {"message": "Reset complete."}
    response = client.get("http://localhost:51225/v1/reset_app/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == answer


def test_reset_fail():
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb72123"
    answer = {"message": "Reset failed."}
    response = client.get("http://localhost:51225/v1/reset_app/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == answer


def test_load_db():
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c"
    response = client.get("http://localhost:51225/v1/load_db/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == {"message": "Data added for dates 2021/6/14 - 2021/6/16."}


def test_load_db_fail():
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb1234c"
    response = client.get("http://localhost:51225/v1/load_db/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == {"message": "Operation failed."}


def test_load_db_prod():
    main.environment = "prod"
    pw = "9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c"
    response = client.get("http://localhost:51225/v1/load_db/", params={"password_hexdigest": pw, 'session': t_session})
    assert response.json() == {"message": "Method not allowed in production."}


# test on registering
def test_register():
    name = "aaa123"
    email = "bbb@aaa"
    id = "bbb123"
    pw = "ccc"
    _type = "client"
    response = client.post("http://localhost:51225/v1/register/", params={"name": name, "email": email, "id": id, "pw": pw, "_type": _type})
    print(response.json())
    assert 'message' not in response.json() 


# test on login
def test_login():
    id = "bbb123"
    pw = "ccc"
    _type = "client"
    response = client.get("http://localhost:51225/v1/login/", params={"id": id, "pw": pw, "_type": _type})
    answer = {"id": 11, "user_id": id, "active": 1}
    if main.client_login == 1:
        assert 'message' not in response.json()
    else:
        assert response.json() == {"message": "Client login not allowed."}


# test on deactivation
def test_deactivate_client():
    id = "bbb123"
    response = client.post("http://localhost:51225/v1/deactivate/", params={"user_id": id, 'session': t_session})
    answer = {"user_id": id}
    assert response.json() == answer


def test_deactivate_client_invalid():
    id = "ccc"
    response = client.post("http://localhost:51225/v1/deactivate/", params={"user_id": id, 'session': t_session})
    answer = {"message": "Invalid client id"}
    assert response.json() == answer


# test on activation
def test_activate_client():
    id = "bbb123"
    response = client.post("http://localhost:51225/v1/activate/", params={"user_id": id, 'session': t_session})
    answer = {"user_id": id}
    assert response.json() == answer


def test_activate_client_invalid():
    id = "ccc"
    response = client.post("http://localhost:51225/v1/activate/", params={"user_id": id, 'session': t_session})
    answer = {"message": "Invalid client id"}
    assert response.json() == answer


# test register_manager with toggle
def test_register_manager():
    name = "man"
    id = "bbb12345"
    pw = "ccc"
    _type = "manager"
    response = client.post("http://localhost:51225/v1/register_manager/", params={"name": name, "id": id, "pw": pw, "_type": _type})
    if main.manager_registration == 1:
        assert 'id' in response.json()
    else:
        assert response.json() == {"message": "Manager registration not allowed."}

# test report saving
def test_add_report_history():
    parameters = {
        "id": 1,
        "search_id": "1",
        "search_start": datetime.strptime("2022-01-01", "%Y-%m-%d"),
        "search_end": datetime.strptime("2022-12-31", "%Y-%m-%d"),
        "search_type": "reservation",
        'session': t_session
    }

    response = client.post("http://localhost:51225/v1/report_history/", params=parameters)
    assert response.json() == {"id": 1}


def test_get_report_history():
    parameters = {
        "id": 1,
        "search_type": "reservation",
        'session': t_session
    }
    response = client.get("http://localhost:51225/v1/report_history/", params=parameters)
    result = json.loads(response.json())
    assert result == [['1', '2022-01-01 00:00:00', '2022-12-31 00:00:00']]

def test_tear_down():
    db = main.db
    cursor = db.conn.cursor()
    with db.conn:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM reservations")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM history")
