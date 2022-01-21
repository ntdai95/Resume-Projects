from datetime import datetime
from database import Database
from reservation import Program


db = Database("tests/testing")
program = Program(db)


def test_check_db_for_reservation_machine1():
    datetime_list = [datetime(year=2021, month=1, day=1)]
    machine = "harvest"
    result = program._check_db_for_reservation_machine(datetime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_db_for_reservation_machine2():
    datetime_list = [datetime(year=2021, month=1, day=1)]
    machine = "irrad1"
    result = program._check_db_for_reservation_machine(datetime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_db_for_reservation_machine3():
    datetime_list = [datetime(year=2021, month=1, day=1)]
    machine = "irrad2"
    result = program._check_db_for_reservation_machine(datetime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_db_for_reservation_machine4():
    datetime_list = [datetime(year=2021, month=1, day=1)]
    machine = "crusher"
    result = program._check_db_for_reservation_machine(datetime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_db_for_reservation_machine_already_reserved():
    reservation_id = "c2e10f2a-6604-4c8e-9e2c-9e0c31b0dc33"
    customer_id = "1"
    datetime_list = [datetime(year=2021, month=1, day=1)]
    to_reserve = "harvest"
    db.add_reservations(reservation_id, customer_id, datetime_list, to_reserve)

    result = program._check_db_for_reservation_machine(datetime_list, to_reserve)
    answer = (False, f"This {to_reserve} is already reserved at this time.")
    assert result == answer


def test_check_machine_res_valid_succeed():
    datatime_list = [datetime(year=2021, month=5, day=14, hour=14)]
    machine = "harvest"
    result = program._check_machine_res_valid(datatime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_machine_res_valid_fail():
    datatime_list = [datetime(year=2021, month=5, day=14)]
    machine = "harvest"
    result = program._check_machine_res_valid(datatime_list, machine)
    answer = (False, " Our hours on weekdays are 9am - 6pm")
    assert result == answer


def test_make_machine_reservation_success():
    machine = "harvest"
    cust_id = 1
    reservation_date = "2022-05-12"
    start_time = "11:00"
    end_time = "13:00"
    result = program.make_machine_reservation(machine, cust_id, reservation_date, start_time, end_time)
    assert result["total_cost"] == 13200.0
    assert result["down_payment"] == 6600.0


def test_make_machine_reservation_fail():
    machine = "harvest"
    cust_id = 1
    reservation_date = "2022-05-12"
    start_time = "11:00"
    end_time = "13:00"
    result = program.make_machine_reservation(machine, cust_id, reservation_date, start_time, end_time)
    assert result == {
        'message': 'There is an error with your reservation: This harvest is already reserved at this time. '}


def test_check_db_for_reservation_workshop_fail():
    datetime_list = [datetime(year=2021, month=1, day=1)]
    machine = "harvest"
    result = program._check_db_for_reservation_workshop(datetime_list, machine)
    answer = (False, f"This {machine} is already reserved at this time.")
    assert result == answer


def test_check_db_for_reservation_workshop():
    datetime_list = [datetime(year=2021, month=1, day=2)]
    machine = "harvest"
    result = program._check_db_for_reservation_workshop(datetime_list, machine)
    answer = (True, '')
    assert result == answer


def test_check_facility_open_fail1():
    datetime_list = [datetime(year=2021, month=5, day=13)]
    result = program._check_facility_open(datetime_list)
    answer = (False, "Our hours on weekdays are 9am - 6pm")
    assert result == answer


def test_check_facility_open_fail2():
    datetime_list = [datetime(year=2021, month=5, day=16)]
    result = program._check_facility_open(datetime_list)
    answer = (False, "We are closed on Sundays")
    assert result == answer


def test_check_facility_open_fail3():
    datetime_list = [datetime(year=2021, month=5, day=15)]
    result = program._check_facility_open(datetime_list)
    answer = (False, "Our hours on Saturdays are 10am - 4pm")
    assert result == answer


def test_check_facility_open_success():
    datetime_list = [datetime(year=2021, month=5, day=14, hour=14)]
    result = program._check_facility_open(datetime_list)
    answer = (True, '')
    assert result == answer


def test_check_workshop_res_valid_success():
    datetime_list = [datetime(year=2021, month=5, day=14, hour=14)]
    things_to_reserve = "harvest"
    result = program._check_workshop_res_valid(datetime_list, things_to_reserve)
    answer = (True, '')
    assert result == answer


def test_check_workshop_res_valid_fail():
    datetime_list = [datetime(year=2021, month=5, day=14)]
    things_to_reserve = "harvest"
    result = program._check_workshop_res_valid(datetime_list, things_to_reserve)
    answer = (False, " Our hours on weekdays are 9am - 6pm")
    assert result == answer


def test_calculate_downpayment_workshop():
    thing_to_reserve = "workshop1"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (49.5, 24.75)
    assert answer == result


def test_calculate_downpayment_microv():
    thing_to_reserve = "microv1"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (1000.0, 500.0)
    assert answer == result


def test_calculate_downpayment_irrad():
    thing_to_reserve = "irrad1"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (1100.0, 550.0)
    assert answer == result


def test_calculate_downpayment_extrud():
    thing_to_reserve = "extrud1"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (250.0, 125.0)
    assert answer == result


def test_calculate_downpayment_crusher():
    thing_to_reserve = "crusher"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (10000, 5000.0)
    assert answer == result


def test_calculate_downpayment_harvest():
    thing_to_reserve = "harvest"
    time_list = [datetime(year=2021, month=5, day=14)]
    result = program._calculate_downpayment(thing_to_reserve, time_list)
    answer = (4400.0, 2200.0)
    assert answer == result


def test_make_workshop_reservation():
    workshop_number = 1
    cust_id = 2
    reservation_date = "2022-05-12"
    start_time = "13:00"
    end_time = "14:00"
    result = program.make_workshop_reservation(workshop_number, cust_id, reservation_date, start_time, end_time)
    assert result["total_cost"] == 74.25
    assert result["down_payment"] == 37.125


def test_make_workshop_reservation_fail():
    workshop_number = 1
    cust_id = 2
    reservation_date = "2022-05-12"
    start_time = "13:00"
    end_time = "14:00"
    result = program.make_workshop_reservation(workshop_number, cust_id, reservation_date, start_time, end_time)
    assert result == {
        'message': 'There is an error with your reservation: This workshop1 is already reserved at this time. '}


def test_cancel_reservation():
    info = program.make_workshop_reservation(1, 1, "2022-05-06", "13:00", "14:00")
    result = program.cancel_reservation(info["reservation_id"])
    assert result["reservation_id"] == info["reservation_id"]
    assert result["refund"] == 27.84375