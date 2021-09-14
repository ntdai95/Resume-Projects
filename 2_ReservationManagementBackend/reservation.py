import uuid
import json
from datetime import datetime, timedelta, time
from pytz import timezone
from database import Database
from typing import Dict, Any, List, Tuple


class Program:
    """Program class

    The main engine for running the system. Stores a connection to the DB and reads/writes to it.
    """
    def __init__(self, db: Database):
        self.db = db
        self._load_config()

    def _load_config(self) -> None:
        """Load config

        Internal function to load the config file settings.
        """
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.client_login = config['options']['client_login']
            self.manager_registration = config['options']['manager_registration']
            self.environment = config['environment']

    def _check_machine_res_valid(self, 
            datetime_list: List[datetime], 
            machine: str) -> Tuple[bool, str]:
        """Check machine reservation valid

        Check if machine reservation is valid.

        Args:
            datetime_list: a list of datetimes to check
            machine: the machine to check against
        Returns:
            Tuple of bool plus a reason or empty string
        """
        res_valid, res_message = self._check_db_for_reservation_machine(datetime_list, machine)
        facil_valid, facil_message = self._check_facility_open(datetime_list)
        if not res_valid or not facil_valid:
            print("ERROR MESSAGES: ", res_message, facil_message)
            return (False, res_message + " " + facil_message)
        return (True, "")


    def make_machine_hold(self, 
            machine: str,
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str,
            held_for_user: str) -> Dict[str, Any]:
        """
        Make a machine hold
        """
        reservation_id = str(uuid.uuid4())
        datetime_list = []

        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')

        time_delta = start_day_end_time - start_datetime

        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]

        valid, error = self.check_machine_res_valid(datetime_list, machine)

        if not valid:
            return {"message": f"There is an error with your hold: {error}"}
        else:
            self.db.add_hold(reservation_id, cust_id, datetime_list, machine, held_for_user)
            print(f"Machine hold successful!\n - Reservation ID: {reservation_id}\n")
            return {
                "total_cost": 0, 
                "down_payment": 0,
                "facility_requested": cust_id,
                "held_for_user": held_for_user,
                "reservation_id": reservation_id}


    def make_machine_reservation(self, 
            machine: str,
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str) -> Dict[str, Any]:
        """
        Make a machine reservation
        """
        reservation_id = str(uuid.uuid4())
        datetime_list = []

        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')

        time_delta = start_day_end_time - start_datetime

        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]

        valid, error = self.check_machine_res_valid(datetime_list, machine)

        if not valid:
            return {"message": f"There is an error with your reservation: {error}"}
        else:
            total_cost, down_payment = self.calculate_downpayment(machine, datetime_list)
            transaction_type = "Reserve"
            print("datetime_list", datetime_list, "\n")

            self.db.add_reservations(reservation_id, cust_id, datetime_list, machine)
            self.db.add_transaction(cust_id, reservation_id, transaction_type, total_cost, 
                                    down_payment, datetime_list[0])
            print(f"Machine reservation successful!\n - Reservation ID: {reservation_id}\n" +
                  f" - Total cost: ${total_cost}\n - Total down payment: ${down_payment}\n")
            return {
                "total_cost": total_cost, 
                "down_payment": down_payment, 
                "reservation_id": reservation_id}


    def _check_workshop_res_valid(self, datetime_list: List[datetime], thing_to_reserve: str) -> Tuple[bool, str]:
        """Check workshop res valid

        Check if a workshop reservation is valid.

        Args:
            datetime_list: a list of datetimes
            thing_to_reserve: the thing to check against
        Returns:
            tuple of success plus message or empty string
        """
        res_valid, res_message = self._check_db_for_reservation_workshop(datetime_list, thing_to_reserve)
        facil_valid, facil_message = self._check_facility_open(datetime_list)
        if not res_valid or not facil_valid:
            print("ERROR MESSAGES: ", res_message, facil_message)
            return (False, res_message + " " + facil_message)
        return (True, "")


    def _check_facility_open(self, datetime_list: List[datetime]) -> Tuple[bool, str]:
        """Check facility open

        Checks if the times in the datetime_list passed in include any times that are outside of the
        bounds of the "open times" of the facility.

        Args:
            datetime_list: a list of datetimes to check
        Returns:
            If the times are valid, returns a tuple of (True, "")
            If any of the times in the list are invalid, it will return a tuple of the value False, 
            and an error message.
        """
        weekday_open = time(9, 00, 00)
        weekday_last_res = time(18, 00, 00)
        weekend_open = time(10, 00, 00)
        weekend_last_res = time(16, 00,00)
        for reservation in datetime_list:
            if reservation.weekday() == 6: #sunday
                return (False, "We are closed on Sundays")
            elif reservation.weekday() == 5: #friday
                if reservation.time() < weekend_open or reservation.time() > weekend_last_res:
                    print("reservation.time() bad", reservation.time())
                    return (False, "Our hours on Saturdays are 10am - 4pm")
            else:
                if reservation.time() < weekday_open or reservation.time() > weekday_last_res:
                    print("reservation.time() bad", reservation.time())
                    return (False, "Our hours on weekdays are 9am - 6pm")
        return (True, "")

    def _check_db_for_reservation_machine(self, 
            datetime_list: List[datetime], 
            machine: str) -> Tuple[bool, str]:
        """Check db for reservation machine

        Checks the database if the times in the datetime_list passed in include any times where the 
        thing to reserve is already reserved. 
        
        Args:
            datetime_list: a list of datetimes
            machine: the machine to reserve
        Returns:
            If the times are valid, returns a tuple of (True, "")
            If any of the times in the list are invalid, it will return a tuple of the value False, 
            and an error message.
        """
        reservations = self.db.get_reservations_given_list(datetime_list, machine)
        if len(reservations) > 0:
            return (False, f"This {machine} is already reserved at this time.")
        return (True, "")


    def _check_db_for_reservation_workshop(self, 
            datetime_list: List[datetime], 
            thing_to_reserve: str) -> Tuple[bool, str]:
        """Check db for reservation workshop

        Checks the database if the times in the datetime_list passed in include any times where the
        thing to reserve is already reserved.

        Args:
            datetime_list: the list of datetimes to check
            thing_to_reserve: the thing to check reservations for
        Returns:
            If the times are valid, returns a tuple of (True, "")
            If any of the times in the list are invalid, it will return a tuple of the value False, 
            and an error message.
        """
        reservations = self.db.get_reservations_given_list(datetime_list, thing_to_reserve)
        if len(reservations) > 0:
            return (False, f"This {thing_to_reserve} is already reserved at this time.")
        return (True, "")


    def _calculate_downpayment(self, 
            thing_to_reserve: str, 
            datetime_list: List[datetime]) -> Tuple[float, float]:
        """Calculate downpayment

        Calculates a downpayment for reservations and holds.

        Args:
            thing_to_reserve: the thing to reserve for cost
            datetime_list: to know how many chunks of time
        Returns:
            A tuple of total_cost and down_payment
        """
        total_cost = 0
        now = datetime.now(timezone('America/Chicago'))
        min_date = min(datetime_list)
        if (timezone('America/Chicago').localize(min_date) - now) >= timedelta(days=14):
            discount = 0.75
        else:
            discount = 1
        for _ in datetime_list:
            if "workshop" in thing_to_reserve:
                total_cost = total_cost + ((99 / 2) * discount)
            elif "microv" in thing_to_reserve:
                total_cost = total_cost + ((2000 / 2) * discount)
            elif "irrad" in thing_to_reserve:
                total_cost = total_cost + ((2200 / 2) * discount)
            elif "extrud" in thing_to_reserve:
                total_cost = total_cost + ((500 / 2) * discount)
            elif thing_to_reserve == "crusher":
                total_cost = total_cost + (10000 * discount)
            elif thing_to_reserve == "harvest":
                total_cost = total_cost + ((8800 / 2) * discount)
        down_payment = total_cost / 2
        return (total_cost, down_payment)


    def make_machine_reservation(self, 
            machine: str,
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str) -> Dict[str, Any]:
        """Make machine reservation

        Make a machine reservation.

        Args:
            machine: machine to reserve
            cust_id: the customer id to keep on reservation
            reservation_date: the date to reserve
            start_time: the start time
            end_time: the end time
        Returns:
            A json with cost info or error
        """
        reservation_id = str(uuid.uuid4())
        datetime_list = []
        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')
        time_delta = start_day_end_time - start_datetime
        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]
        valid, error = self._check_machine_res_valid(datetime_list, machine)
        if not valid:
            return {"message": f"There is an error with your reservation: {error}"}
        else:
            total_cost, down_payment = self._calculate_downpayment(machine, datetime_list)
            transaction_type = "Reserve"
            print("datetime_list", datetime_list, "\n")
            self.db.add_reservations(reservation_id, cust_id, datetime_list, machine)
            self.db.add_transaction(cust_id, reservation_id, transaction_type, total_cost, 
                                    down_payment, datetime_list[0])
            print(f"Machine reservation successful!\n - Reservation ID: {reservation_id}\n" +
                  f" - Total cost: ${total_cost}\n - Total down payment: ${down_payment}\n")
            return {
                "total_cost": total_cost, 
                "down_payment": down_payment, 
                "reservation_id": reservation_id}


    def make_machine_hold(self, 
            machine: str,
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str,
            held_for_user: str) -> Dict[str, Any]:
        """Make machine hold

        Make a machine hold which is similar to reservation but externally created.

        Args:
            machine: the machine to hold
            cust_id: client_id making hold
            reservation_date: the date of reservation hold
            start_time: starting time
            end_time: ending time
            held_for_user: the user the reservation is held for
        Returns:
            json with hold info or error message
        """
        reservation_id = str(uuid.uuid4())
        datetime_list = []
        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')
        time_delta = start_day_end_time - start_datetime
        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]
        valid, error = self._check_machine_res_valid(datetime_list, machine)
        if not valid:
            return {"message": f"There is an error with your hold: {error}"}
        else:
            self.db.add_hold(reservation_id, cust_id, datetime_list, machine, held_for_user)
            print(f"Machine hold successful!\n - Reservation ID: {reservation_id}\n")
            return {
                "total_cost": 0, 
                "down_payment": 0,
                "facility_requested": cust_id,
                "held_for_user": held_for_user,
                "reservation_id": reservation_id}


    def make_workshop_reservation(self, 
            workshop_number: str, 
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str) -> Dict[str, Any]:
        """Make workshop reservation

        Make a workshop reservation.

        Args:
            workshop_number: workshop to reserve
            cust_id: user making the reservation
            reservation_date: the date of the reservation
            start_time: starting time
            end_time: ending time
        Returns:
            json of reservation info
        """
        reservation_id = str(uuid.uuid4())
        total_cost = 0
        down_payment = 0
        thing_to_reserve = f"workshop{workshop_number}"
        datetime_list = []
        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')
        time_delta = start_day_end_time - start_datetime
        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]
        valid, error = self._check_workshop_res_valid(datetime_list, thing_to_reserve)
        if not valid:
            return {"message": f"There is an error with your reservation: {error}"}
        else:
            total_cost, down_payment = self._calculate_downpayment(thing_to_reserve, datetime_list)
            transaction_type = f"Reserve workshop {workshop_number}"
            self.db.add_reservations(reservation_id, cust_id, datetime_list, 
                                     f'workshop{workshop_number}')
            self.db.add_transaction(cust_id, reservation_id, transaction_type, total_cost, 
                                    down_payment, datetime_list[0])
        print(f"Workshop reservation successful!\n - Reservation ID: {reservation_id}\n" +
              f"Total cost: ${total_cost}\nTotal down payment: ${down_payment}\n")
        return {
            "total_cost": total_cost, 
            "down_payment": down_payment, 
            "reservation_id": reservation_id}


    def make_workshop_hold(self, 
            workshop_number: str,
            cust_id: str, 
            reservation_date: str, 
            start_time: str, 
            end_time: str,
            held_for_user: str) -> Dict[str, Any]:
        """Make workshop hold

        Make a workshop hold similar to reservation.

        Args:
            workshop_number: workshop to hold
            cust_id: user making the hold
            reservation_date: the date of the hold
            start_time: starting time
            end_time: ending time
            held_for_user: the user the hold is for
        Returns:
            json of hold info
        """
        reservation_id = str(uuid.uuid4())
        thing_to_reserve = f"workshop{workshop_number}"
        datetime_list = []
        start_datetime = datetime.strptime((reservation_date + " " + start_time),'%Y-%m-%d %H:%M')
        start_day_end_time = datetime.strptime((reservation_date + " " + end_time),'%Y-%m-%d %H:%M')
        time_delta = start_day_end_time - start_datetime
        for y in [y for y in range(time_delta.seconds + 1) if y % 1800 == 0]:
            datetime_list.append(start_datetime + timedelta(seconds=y))
        datetime_list = datetime_list[0:-1]
        valid, error = self._check_workshop_res_valid(datetime_list, thing_to_reserve)
        if not valid:
            return {"message": f"There is an error with your hold: {error}"}
        else:
            self.db.add_hold(reservation_id, cust_id, datetime_list, f'workshop{workshop_number}', held_for_user)
            print(f"Workshop hold successful!\n - Reservation ID: {reservation_id}\n")
            return {
                "total_cost": 0, 
                "down_payment": 0,
                "facility_requested": cust_id,
                "held_for_user": held_for_user,
                "reservation_id": reservation_id}


    def cancel_reservation(self, reservation_id: str) -> Dict[str, Any]:
        """Cancel reservation

        Cancel a reservation and refund any money for it.

        Args:
            reservation_id: the uuid for reservation
        Returns:
            json of reservation_id and refund
        """
        response = self.db.get_transaction(reservation_id)
        if response == []:
            return {"message": "This reservation does not exist or was already canceled."}
        cust_id = response[0][1]
        cost = response[0][2]
        downpayment = cost / 2
        transaction_datetime = datetime.strptime(response[0][3].split(" ")[0],'%Y-%m-%d')
        now = datetime.now(timezone('America/Chicago'))
        now_as_string = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
        formatted_now = datetime.strptime(now_as_string,'%Y-%m-%d %H:%M')
        delta = timezone('America/Chicago').localize(transaction_datetime) - now
        if delta.days >= 7:
            refund = 0.75 * downpayment
        elif delta.days >= 2:
            refund = 0.5 * downpayment
        else:
            refund = 0
        transaction_type = "Cancel"
        self.db.delete_reservation(reservation_id)
        self.db.add_transaction(cust_id, reservation_id, transaction_type, -refund, 0, formatted_now)
        print(f"Cancellation successful!\n - Reservation ID: {reservation_id}\n" +
              f"- Total refund: ${refund}\n")
        return {"reservation_id": reservation_id, "refund": refund}
