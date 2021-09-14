from uuid import UUID
import pandas as pd
import json
import smtplib
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

class client:
    """Client class

    Holds all client flow and interactions
    """

    def __init__(self, url: str = 'http://localhost:51225'):
        """Init method

        Args:
            url: the base url that the server is located at with port
        """
        self.base_url = url
        self.session = ''
        self.cli_login_active = False
        self._get_cli_init()
        self.user_id = ''

    #######################
    #   Internal Helpers  #
    #######################

    def _get_cli_init(self) -> None:
        """Get the CLI client login initilized status

        Sets self.cli_login_active to be the same as server setting.
        """
        response = requests.get(f'{self.base_url}/v1/login_status/')
        res = response.json()
        if res['client_login'] == 1:
            self.cli_login_active = True
        else:
            self.cli_login_active = False

    def _version_uuid(self, uuid: str) -> bool:
        """Check for valid UUID4 input

        Args:
            uuid: a string provided that should be a uuid
        Returns:
            true: this is a valid uuid4
            false: this is not a valid uuid4
        """
        try:
            res = UUID(uuid).version
            if res == 4:
                return True
            else:
                return False
        except ValueError:
            return False

    #######################
    #   Shared Functions  #
    #######################

    def _edit_reservation(self, client_id: int) -> None:
        """Edit a reservation
        
        Edit a reservation and change the date and time.

        Args:
            client_id: client_id of the account to be effected
        """
        print("Edit a Reservation")
        print("=" * 40)
        reservation_id = input("Please, enter the reservation id\n --> ")
        check = self._version_uuid(reservation_id)
        if check:
            # valid uuid format
            parameters = {"reservation_id": reservation_id, "session": self.session}
            response = requests.get(f'{self.base_url}/v1/reservations/{reservation_id}', params=parameters)
            json_object = response.json()
            json_list = json.loads(json_object)[0]
            print(f"Your current reservation is for {json_list[3]}, starting at {json_list[2]}.")
            start_date = input("What date do you want your reservation instead? "
                               "(yyyy-mm-dd)\n --> ")
            start_time = input("What time do you want to start the reservation instead? "
                               "(HH:MM)\n --> ")
            end_time = input("What time do you want to end the reservation instead? (HH:MM, "
                             "inclusive; min. 1 hour; please enter a time range within normal "
                             "business hours)\n --> ")
            parameters = {"thing_to_reserve": json_list[3],
                          "reservation_date": start_date,
                          "start_time": start_time,
                          "end_time": end_time,
                          "customer_id": client_id,
                          "session": self.session}
            response = requests.post(f'{self.base_url}/v1/reservations/', params=parameters)
            json_object = response.json()
            if isinstance(json_object, dict):
                if 'message' not in json_object.keys():
                    print("\nNew Reservation Details Below")
                    print("=" * 40)
                    print("New reservation ID: {}".format(json_object['reservation_id']))
                    total_cost = float("{:.2f}".format(json_object.get('total_cost', 0)))
                    downpayment = float("{:.2f}".format(json_object.get('down_payment', 0)))
                    parameters = {"reservation_id": reservation_id, 
                                    "session": self.session}
                    response = requests.delete(f'{self.base_url}/v1/reservations/', params=parameters)
                    json_object = response.json()
                    refund = float("{:.2f}".format(json_object.get('refund', 0)))
                    amount_difference = float("{:.2f}".format(refund - total_cost))
                    parameters = {"user_id": self.user_id, "amount": amount_difference, "session": self.session}
                    response = requests.post(f'{self.base_url}/v1/funds', params=parameters)
                    json_object = response.json()
                    print(f"Your new total reservation cost will be ${total_cost}")
                    print(f"Your new down payment will be ${downpayment}")
                    print(f"The total difference in down payments after the edit is ${amount_difference}")
                    print(f"Your new account balance is ${json_object['account_balance']}")
                else:
                    print("\nError")
                    print(response.json()['message'])
        else:
            print("This is not a valid reservation id.")

    def _cancel_reservation(self, client_id: int) -> None:
        """Cancel a reservation
        
        Cancels a reservation using the reservation id.

        Args:
            client_id: client_id of the account to be effected
        """
        print("Cancel a Reservation")
        print("=" * 40)
        reservation_id = input("Please, enter the reservation id\n --> ")
        check = self._version_uuid(reservation_id)
        if check:
            parameters = {"reservation_id": reservation_id, "session": self.session}
            response = requests.delete(f'{self.base_url}/v1/reservations/', params=parameters)
            json_object = response.json()
            print("Reservation cancelled\n")
            print(json.dumps(json_object, indent=5))
            refund = json_object.get('refund', 0)
            refund = float(refund)
            parameters = {"user_id": client_id, "amount": refund, "session": self.session}
            response = requests.post(f'{self.base_url}/v1/funds', params=parameters)
            json_object = response.json()
            print("=" * 40)
            print("Your new account balance")
            print("User: {}".format(json_object["user"]))
            print("Account Balance: {}".format(json_object["account_balance"]))
        else:
            print("This is not a valid reservation id.")

    def _add_funds(self, client_id: int) -> None:
        """Add funds to a client account

        Args:
            client_id: client_id of the account to be effected
        """
        print("Add Funds")
        print("=" * 40)
        while True:
            to_add = input("How much would you like to add?\n")
            try:
                to_add = float(to_add)
            except:
                print('Please use numeric digits.')
            if to_add > 25000 or to_add < 1:
                print("Please set a value between $1 and $25,000")
            else:
                break
        parameters = {"user_id": client_id, "amount": to_add, "session": self.session}
        response = requests.post(f'{self.base_url}/v1/funds', params=parameters)
        json_object = response.json()
        print("=" * 40)
        print("New account balance for user: {}".format(json_object["user"]))
        print("Account Balance: {}".format(json_object["account_balance"]))

    def _reservation_report(self, client_id: int = 0, all: bool = False) -> None:
        """Generate reservation report

        This function generates a reservation report and displays it.

        Args:
            client_id: id of the user we are searching
            all: flag for whether to get all clients or only some
        """
        while True:
            choice = input("1 = Write the date interval \n"
                        "2 = Choose from previous search log \n"
                        "Cancel = cancel \n"
                        "--> ")
            if choice == "1":
                # using an input date interval
                start_date = input("What beginning date do you want to pull transaction data? "
                                   "(yyyy-mm-dd)\n --> ")
                end_date = input("What ending date do you want to pull transaction data? "
                                "(yyyy-mm-dd, inclusive)\n --> ")
                break
            elif choice == "2":
                # using a saved search
                parameters = {"id": self.user_id, "search_type": "reservation", "session": self.session}
                response = requests.get(f'{self.base_url}/v1/report_history', params=parameters)
                candidate_list = json.loads(response.json())
                if len(candidate_list) == 0:
                    print("There is no search history")
                    continue
                candidates = ""
                for i in range(len(candidate_list)):
                    candidates += "{} = client ID.{}: {} ~ {}\n".format(i+1, candidate_list[i][0], candidate_list[i][1], candidate_list[i][2])
                candidates += "--> "
                while True:
                    cand_choice = input(candidates)
                    if cand_choice.isdigit() and 1 <= int(cand_choice) <= len(candidate_list):
                        cand_choice = int(cand_choice)
                        break
                    else:
                        print("Invalid format. Choose the history again")
                client_id, start_date, end_date = candidate_list[cand_choice-1]
                if client_id == "ALL":
                    all = True
                break
            elif choice == "cancel":
                return
            else:
                print("Please choose 1 or 2.")
        if not all:
            parameters = {"start": start_date,
                        "end": end_date,
                        "customer_id": client_id,
                        "session": self.session}
        else:
            parameters = {"start": start_date,
                        "end": end_date,
                        "session": self.session}
        response = requests.get(f'{self.base_url}/v1/reservations/', params=parameters)
        json_object = response.json()
        if isinstance(json_object, dict):
            print(json_object['message'])
            return
        else:
            return_list = json.loads(json_object)
            df = pd.DataFrame()
            for item in return_list:
                print("Reservation id: {}, 30-minute block start time: {}, item to reserve: {}".format(item[0], item[2], item[3]))
                df = df.append(
                    {"Reservation id": item[0], "30-minute block start time": str(item[2]), "item to reserve": item[3]},
                    ignore_index=True)
            if choice == "1":
                parameters = {"id": id,
                                "search_start": start_date,
                                "search_end": end_date,
                                "search_type": "reservation",
                                "session": self.session}
            if all:
                parameters["search_id"] = "ALL"
            else:
                parameters["search_id"] = client_id
            requests.post(f"{self.base_url}/v1/report_history", params=parameters)
        while True:
            save_option = input("Do you want to save reservation_report.csv? \n[1] yes [2] no -> ")
            if save_option == "1":
                if all:
                    df.to_csv("all_reservation_report({}~{}).csv".format(start_date, end_date), index=False)
                else:
                    df.to_csv("id{}_reservation_report({}~{}.csv".format(client_id, start_date, end_date), index=False)
            break

    def _transaction_report(self, client_id: int = 0, all: bool = False) -> None:
        print("Generate Transaction Report")
        print("=" * 40)

        while True:
            choice = input("1. Write the date interval \n"
                        "2. Choose from previous search log \n"
                        "--> ")
            if choice == "1":
                start_date = input("What beginning date do you want "
                                "to pull transaction data? "
                                "(yyyy-mm-dd)\n --> ")
                end_date = input("What ending date do you want to "
                                "pull transaction data? "
                                "(yyyy-mm-dd,inclusive)\n --> ")
                parameters = {"id": self.user_id,
                            "search_start": start_date,
                            "search_end": end_date,
                            "search_type": "transaction",
                            "session": self.session}
                if all:
                    parameters["search_id"] = "ALL"
                else:
                    parameters["search_id"] = client_id
                requests.post(f"{self.base_url}/v1/report_history", params=parameters)
                break
            elif choice == "2":
                parameters = {"id": self.user_id, "search_type": "transaction", "session": self.session}
                response = requests.get(f"{self.base_url}/v1/report_history",
                                        params=parameters)
                candidate_list = json.loads(response.json())
                if len(candidate_list) == 0:
                    print("There is no history")
                    continue
                candidates = ""
                for i in range(len(candidate_list)):
                    candidates += "{}. client ID.{}: {} ~ {}\n".format(i + 1, candidate_list[i][0], candidate_list[i][1], candidate_list[i][2])
                candidates += "--> "
                while True:
                    cand_choice = input(candidates)
                    if cand_choice.isdigit() and 1 <= int(cand_choice) <= len(candidate_list):
                        cand_choice = int(cand_choice)
                        break
                    else:
                        print("Invalid format. Choose from the numbered options below")
                client_id, start_date, end_date = candidate_list[cand_choice - 1]
                if client_id == "ALL":
                    all = True
                break
            else:
                print("Please choose 1 or 2.")
        if not all:
            parameters = {"start": start_date, "end": end_date, "customer_id": client_id, "session": self.session}
        else:
            parameters = {"start": start_date, "end": end_date, "session": self.session}
        response = requests.get(f'{self.base_url}/v1/transactions/', params=parameters)
        df = pd.DataFrame()
        json_object = response.json()
        if isinstance(json_object, dict):
            print(json_object['message'])
            return
        result_list = json.loads(json_object)
        for item in result_list:
            print(f"Transaction id: {item[0]}, reservation id: {item[2]}, type: {item[3]}, total cost: {item[4]}")
            df = df.append({"Transaction id": item[0], "reservation id": item[2], "type": item[3], 
                            "total cost": item[4]}, ignore_index=True)
        while True:
            save_option = input("Do you want to Save to transaction_report.csv? \n[1] yes [2] no -> ")
            if save_option == "1":
                if all:
                    df.to_csv("all_transaction_report({}~{}).csv".format(start_date, end_date), index=False)
                else:
                    df.to_csv("id{}_transaction_report({}~{}.csv".format(client_id, start_date, end_date), index=False)
                break
            elif save_option == "2":
                break
            else:
                print("Please choose 1 or 2.")

    #######################
    #   Client Functions  #
    #######################

    def _make_reservation(self) -> None:
        """Make a new reservation

        Gets reservation input, validates, and attempts to make a new reservation in our own
        facility first, then randomly chooses another facility if we are booked until we find an 
        open space or there are not open spaces.
        """
        print("Make a Reservation")
        print("=" * 40)
        while True:
            thing_to_reserve = input("What do you want to reserve? \n"
                "(options: \n\tmicrov1(2,000/hr), \n\tmicrov2(2,000/hr), \n\tirrad1(2,200/hr), "
                "\n\tirrad2(2,200/hr), \n\textrud1(500/hr), \n\textrud2(500/hr), \n\tcrusher(20,000/hr), "
                "\n\tharvest(8,800/hr), \n\tworkshop1(99/hr), \n\tworkshop2(99/hr), "
                "\n\tworkshop3(99/hr),\n\tworkshop4(99/hr)) \n->")
            things = {"microv1", "microv2", "irrad1", "irrad2", "extrud1", "extrud2", "crusher", 
                      "harvest", "workshop1", "workshop2", "workshop3", "workshop4"}
            if thing_to_reserve in things:
                break
            print("Our facility only has the following equipments/workshops: "
                "microv1, microv2, irrad1, irrad2, extrud1, extrud2, "
                "crusher, harvest, workshop1, workshop2, workshop3, or workshop4")
        reserving = True
        while reserving:
            reservation_date = input("\nWhat date do you want to do your reservation? (yyyy-mm-dd, "
                                    "Our facility does not support recurring reservations.)\n -->")
            start_time = input("What time do you want to start the reservation? (HH:MM)\n --> ")
            end_time = input("What time do you want to end the reservation? (HH:MM, inclusive; "
                            "min. 1 hour; please enter a time range within normal business "
                            "hours)\n --> ")
            parameters = {
                "thing_to_reserve": thing_to_reserve,
                "reservation_date": reservation_date,
                "start_time": start_time,
                "end_time": end_time,
                "customer_id": self.user_id,
                "session": self.session}
            response = requests.post(f'{self.base_url}/v1/reservations/', params=parameters)
            json_object_reservation = response.json()
            if "message" not in json_object_reservation.keys():
                total_cost = float(json_object_reservation.get('total_cost', 0))
                parameters = {"user_id": self.user_id, "amount": -total_cost, 'session': self.session}
                response = requests.post(f'{self.base_url}/v1/funds', params=parameters)
                json_object_fund = response.json()
                if "message" in json_object_fund.keys():  # removing reservations if low funds
                    print(json_object_fund["message"])
                    parameters = {
                        "reservation_id": json_object_reservation["reservation_id"], 
                        "session": self.session}
                    response = requests.delete(f'{self.base_url}/v1/reservations/', params=parameters)
                else:
                    print("\nReservation success")
                    print("=" * 40)
                    print("Reservation Info")
                    print("reservation id: {}".format(json_object_reservation["reservation_id"]))
                    print("total cost: {}".format(json_object_reservation["total_cost"]))
                print("=" * 40)
                print("Your new account balance")
                print("user: {}".format(json_object_fund["user"]))
                print("account balance: {}".format(json_object_fund["account_balance"]))
                break
            elif f"{thing_to_reserve} is already reserved at this time." in json_object_reservation["message"]:
                print("\nDetails Below")
                print(json_object_reservation["message"] + " (at the facility of APIGROUP5 in Chicago, IL)\n")
                parameters = {"user_id": self.user_id, "session": self.session}
                response = requests.get(f'{self.base_url}/v1/user/', params=parameters)
                json_list = json.loads(response.json())
                client_name = json_list[0][1]
                # standardizing item request to match other facilities' formats
                if thing_to_reserve == "extrud1":
                    thing_to_reserve = "polymer extruder1"
                elif thing_to_reserve == "extrud2":
                    thing_to_reserve = "polymer extruder2"
                elif thing_to_reserve == "crusher":
                    thing_to_reserve = "high velocity crusher"
                elif thing_to_reserve == "microv1":
                    thing_to_reserve = "mini microvac1"
                elif thing_to_reserve == "microv2":
                    thing_to_reserve = "mini microvac2"
                elif thing_to_reserve == "harvest":
                    thing_to_reserve = "1.21 gigawatt lightning harvester"
                elif thing_to_reserve == "irrad1":
                    thing_to_reserve = "irradiator1"
                elif thing_to_reserve == "irrad2":
                    thing_to_reserve = "irradiator2"
                dictionary = {'username': 'team5', 'password': 'password5', 'client_name': client_name, 'request': thing_to_reserve,
                            'start_date': reservation_date, 'start_time': start_time, 'end_time': end_time}
                facility_numbers = [1, 2, 3, 4]
                random.shuffle(facility_numbers)
                while facility_numbers != []:
                    try:
                        facility_number = facility_numbers.pop(0)
                        response = requests.post('http://linux{}.cs.uchicago.edu:5122{}/hold'.format(facility_number, facility_number), json=dictionary)
                        json_object_reservation_other_facility = response.json()
                        if json_object_reservation_other_facility["success"]:
                            break
                    except:
                        pass
                if facility_numbers != [] or (facility_numbers == [] and json_object_reservation_other_facility["success"]):
                    try:
                        print("However, your reservation has been scheduled at " + json_object_reservation_other_facility["facility_name"])
                    except:
                        print("However, your reservation has been scheduled at facility {}".format(facility_number))
                    print("=" * 40)
                    print(json_object_reservation_other_facility["message"])
                    reserving = False
                elif facility_numbers == []:
                    print("Unfortunately, your reservation cannot be made because no resource is available at the requested time at any other facility.")
                    while True:
                        keep_reserving = input("Do you want to select another time for your reservation? [1] yes [2] no --> ")
                        if keep_reserving == "1":
                            break
                        elif keep_reserving == "2":
                            reserving = False
                            break
                        else:
                            print("Please choose 1 or 2")
            else:
                print("\nDetails Below")
                print(json_object_reservation["message"])

    def _edit_profile(self) -> None:
        """Edit profile

        Allows user to change their password or request forgot password.
        """
        print("Edit My Profile")
        print("=" * 40)
        parameters = {"user_id": self.user_id, 'session': self.session}
        response = requests.get(f'{self.base_url}/v1/user/', params=parameters)
        json_object = response.json()
        json_list = json.loads(json_object)
        print("Account details: name={}, username={}, account balance=${}".format(json_list[0][1], json_list[0][2], json_list[0][6]))
        while True:
            pw = input("To make edits, please enter your current password or type 'forgot' if you forgot your password:\n --> ")
            if pw.lower() != "forgot":
                break
            temp_pass = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(12)])
            parameters = {"user_id": self.user_id, "new_pw": temp_pass, "session": self.session}
            response = requests.post(f'{self.base_url}/v1/user/update_password', params=parameters)
            if response.json()["message"] == "Password change successful":
                print("Old password updated to temporary password.")
                client_email = json_list[0][7]
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    subject = 'Request to change your password!'
                    body = "Please, use the following temporary password to change your old forgotten password: {}".format(temp_pass)
                    message = "Subject: {}\n\n{}".format(subject, body)
                    smtp.sendmail(EMAIL_ADDRESS, client_email, message)
                print("Your temporary password has been sent to your email address. Use that to change your old forgotten password.")
            else:
                print("Something went wrong. Therefore, the old password has not been updated to the temporary password. Please, type 'forgot' again.")
        parameters = {"id": json_list[0][2], "pw": pw, "_type": "client", "session": self.session}
        response = requests.post(f'{self.base_url}/v1/login/', params=parameters)
        if "message" in response.json().keys():
            print(response.json()["message"])
            return
        else:
            self.session = response.json()["session"]
            new_pass = input("What would you like to change your password to?\n --> ")
            parameters = {"user_id": self.user_id, "new_pw": new_pass, "session": self.session}
            response = requests.post(f'{self.base_url}/v1/user/update_password', params=parameters)
            print(response.json()["message"])

    def _account_balance(self) -> None:
        """Account balance

        Shows the users account balance
        """
        print("Show My Account Balance")
        print("=" * 40)
        parameters = {"user_id": self.user_id, "session": self.session}
        response = requests.get(f'{self.base_url}/v1/funds', params=parameters)
        json_object = response.json()
        print("Account Balance Below")
        print("user: {}".format(json_object["user"]))
        print("account balance: {}".format(json_object["account_balance"]))

    def client_activity(self) -> None:
        """Client Activity
        
        Client user flow including menu and logout.

        - Show my reservations (at the facility whose interface I'm using)
        - Edit a reservation
        - Make a reservation
        - Cancel a reservation
        - Add funds to my account
        - Show my financial transactions
        - Edit my profile (for example, change my name but don't destroy/detach my history of transactions)
        - Show my account balance
        """
        while True:
            choice = input("\nWhat would you like to do? \n("
                            "1 = Make a reservation\n "
                            "2 = Edit a reservation\n "
                            "3 = Cancel a reservation\n "
                            "4 = List my reservations\n "
                            "5 = Show my account balance \n "
                            "6 = Add funds to my account\n "
                            "7 = List my transactions\n "
                            "8 = Edit my profile \n "
                            "logout = logout)\n -> ")
            if choice == "1":
                self._make_reservation()
            elif choice == "2":
                self._edit_reservation(client_id=self.user_id)
            elif choice == "3":
                self._cancel_reservation(client_id=self.user_id)
            elif choice == "4":
                print("Generate Customer Reservation Report")
                print("=" * 40)
                print("Your User ID is: ", self.user_id)
                self._reservation_report(client_id=self.user_id)
            elif choice == "5":
                self._account_balance()
            elif choice == "6":
                self._add_funds(client_id=self.user_id)
            elif choice == "7":
                self._transaction_report(client_id=self.user_id)
            elif choice == "8":
                self._edit_profile()
            elif choice == "logout":
                self.user_id = None
                self.session = ''
                print('Goodbye')
                return

    #######################
    #  Manager Functions  #
    #######################

    def _activate_client_login(self) -> None:
        """Activate client login

        Enable all client logins server wide.
        """
        self.cli_login_active = True
        parameters = {"new_status": 1, "session": self.session}
        requests.post(f"{self.base_url}/v1/client_login/", params=parameters)
        print("Client Login Activated")

    def _deactivate_client_login(self) -> None:
        """Deactivate client login

        Disable all client logins server wide.
        """
        self.cli_login_active = False
        parameters = {"new_status": 0, "session": self.session}
        requests.post(f"{self.base_url}/v1/client_login/", params=parameters)
        print("Client Login Deactivated")

    def _activate_client_account(self) -> None:
        """Activate client account

        Enable a specific client's account for login.
        """
        client_id = input("which client should be activated (username)? ")
        parameters = {"user_id": client_id, "session": self.session}
        response = requests.post(f"{self.base_url}/v1/activate/", params=parameters)
        if "user_id" in response.json().keys():
            print("Activate client {}".format(response.json()["user_id"]))
        else:
            print(response.json()["message"])

    def _deactivate_client_account(self) -> None:
        """Deactivate client account

        Disable a specific client's account for login.
        """
        client_id = input("which client should be deactivated (username)? ")
        parameters = {"user_id": client_id, "session": self.session}
        response = requests.post(f"{self.base_url}/v1/deactivate/", params=parameters)
        if "user_id" in response.json().keys():
            print("Deactivate client {}".format(response.json()["user_id"]))
        else:
            print(response.json()["message"])

    def _list_clients(self) -> None:
        """List Clients

        List all clients in the system.
        """
        parameters = {"session": self.session}
        response = requests.get(f'{self.base_url}/v1/clients/', params=parameters)
        json_object = response.json()
        if isinstance(json_object, dict):
            print(json_object['message'])
            return
        else:
            return_list = json.loads(json_object)
            for item in return_list:
                print(f"Name: {item[0]}, User_id: {item[1]}, Active: {item[2]}, Funds: {item[3]}")
            option = input("Do you want to save as csv? [1] yes [2] no -> ")
            if option == "1":
                df = pd.DataFrame(return_list, columns=["Name", "User id", "Active", "Funds"])
                df.to_csv("clients.csv", index=False)
                print("Saved the csv file!")
            else:
                print("You chose not to save the csv file")
    
    def _manager_get_reservation(self) -> None:
        """Manager Get Reservation

        Used as a helper for manager only flow of get reservation. Allows you to pull only holds, 
        all reservations, as well as a specific client's reservations.
        """
        while True:
            only_hold = input("Do you want to get only the hold reservations? [1] yes [2] no --> ")
            if only_hold == "1" or only_hold == "2":
                break
            else:
                print("Please choose 1 or 2")
        if only_hold == "1":
            print("Generate Hold Reservation Report")
            print("=" * 40)
            parameters = {"session": self.session}
            response = requests.get(f'{self.base_url}/hold', params=parameters)
            result = json.loads(response.json())
            if result == []:
                print("There is no available hold reservation in this facility as of this moment.")
            else:
                print(result)
        else:
            print("Generate Full Reservation Report")
            print("=" * 40)
            self._reservation_report(client_id=0, all=True)

    def _add_client(self) -> None:
        """Add client

        Used by manager to create a client account.
        """
        print("Add a customer")
        print("=" * 40)
        name = input("What is the customer name? ")
        parameters = {"name": name, "session": self.session}
        response = requests.post(f'{self.base_url}/v1/clients/',
                                params=parameters)
        json_object = response.json()
        print("The customer ID is: {}".format(json_object["customer_id"]))
        new_pass = name
        parameters = {"user_id": json_object["customer_id"], "new_pw": new_pass, "session": self.session}
        response = requests.post(f'{self.base_url}/v1/user/update_password', params=parameters)

    def _edit_client(self) -> None:
        """Edit Client

        Used by manager to edit client accounts. Only have access to add funds.
        """
        print("Edit client account")
        print("=" * 40)
        fchoice = input("Add funds? (y,n) ")
        if fchoice == "y":
            client_id = input("Which client id number? ")
            self._add_funds(client_id)

    def _find_client(self) -> None:
        """Find Client

        Used by manager to do a client search.
        """
        print("Find client account")
        print("=" * 40)
        pname = input("Enter the start of customer name: ")
        parameters = {"pname": pname, "session": self.session}
        response = requests.post(f'{self.base_url}/v1/find_client/',params=parameters)
        json_object = response.json()
        if isinstance(json_object, dict):
            print(json_object['message'])
            return
        else:
            return_list = json.loads(json_object)
            for item in return_list:
                print("ID: {}, Name: {}, user_id: {}".format(item[0], item[1], item[2]))

    def _manager_dashboard(self) -> None:
        """Manager Dashboard

        Used by manager to see current number of sessions, current environment, and whether client
        logins are enabled or disabled system wide.
        """
        print("Manager Dashboard\n")
        print("="*20)
        parameters = {"session": self.session}
        res = requests.get(f'{self.base_url}/v1', params=parameters)
        result = res.json()
        if result['Client_Login'] == 1:
            print(f'Client login: enabled')
        else:
            print(f'Client login: disabled')
        print(f"Environment: {result['Environment']}")
        print(f"Active Sessions: {result['Active']}")
        print("="*20)

    def manager_activity(self) -> None:
        """Manager Activity
        
        Facility manager user flow including menu and logout."""
        while True:
            choice = input("\nWhat would you like to do? \n("
                        "1  = Activate client login\n "
                        "2  = Deactivate client login\n "
                        "3  = List all clients\n "
                        "4  = Find client account\n "
                        "5  = Create new customer\n "
                        "6  = Edit customer account\n "
                        "7  = Activate client\n "
                        "8  = Deactivate client\n "
                        "9  = Get all reservations\n "
                        "10 = Get client reservation report\n "
                        "11 = Edit a Reservation\n "
                        "12 = Cancel a Reservation\n "
                        "13 = Get transaction reports\n "
                        "14 = Manager Dashboard\n "
                        "logout = logout)\n -> ")
            if choice == "1":
                self._activate_client_login()
            elif choice == "2":
                self._deactivate_client_login()
            elif choice == "3":
                self._list_clients()
            elif choice == "4":
                self._find_client()
            elif choice == "5":
                self._add_client()
            elif choice == "6":
                self._edit_client()
            elif choice == "7":
                self._activate_client_account()
            elif choice == "8":
                self._deactivate_client_account()
            elif choice == "9":
                self._manager_get_reservation()
            elif choice == "10":
                while True:
                    client_id = input("Client id for reservation report? ")
                    if client_id.isdigit():
                        break
                    else:
                        print("Wrong client ID format")
                print("Generate Client Reservation Report")
                print("=" * 40)
                self._reservation_report(client_id=client_id)
            elif choice == "11":
                while True:
                    client_id = input("Client id for reservation edit? ")
                    if client_id.isdigit():
                        break
                    else:
                        print("Wrong client ID format")
                self._edit_reservation(client_id=client_id)
            elif choice == "12":
                while True:
                    client_id = input("Client id for reservation cancel? ")
                    if client_id.isdigit():
                        break
                    else:
                        print("Wrong client ID format")
                self._cancel_reservation(client_id=client_id)
            elif choice == "13":
                print("Transaction Reports\n")
                while True:
                    clientt = input("Client ID (n for all)? ")
                    if clientt == "n":
                        self._transaction_report(all=True)
                        break
                    elif clientt.isdigit():
                        self._transaction_report(client_id=clientt)
                        break
                    else:
                        print("Wrong client ID format")
            elif choice == "14":
                self._manager_dashboard()
            elif choice == "logout":
                self.session = ''
                self.user_id = ''
                print("Goodbye")
                return

    #######################
    #    Base Program     #
    #######################

    def _manager_login_flow(self) -> None:
        """Manager login flow

        Includes ability to login as manager and create account if enabled.
        """
        print("\n" + "=" * 5 + "Facility Manager Access" + "=" * 5)
        is_register = input("Do you have account? yes or no: \n")
        # process of login
        if is_register == "yes":
            _id = input("username: ")
            pw = input("password: ")
            parameters = {"id": _id, "pw": pw, "_type": "manager"}
            response = requests.post(f'{self.base_url}/v1/login/', params=parameters)
            if "message" in response.json().keys():
                print(response.json()["message"])
                return
            else:
                print("Login success! Hello {}".format(response.json()["user_id"]))
                self.session = response.json()["session"]
                self.user_id = response.json()["id"]
                self.manager_activity()
        # process of registering a manager
        elif is_register == "no":
            name = input("What is your name? ")
            id = input("New username: ")
            pw = input("New password: ")
            parameters = {"name": name, "id": id, "pw": pw, "_type": "manager"}
            response = requests.post(
                f"{self.base_url}/v1/register_manager/", params=parameters)
            if "message" in response.json().keys():
                print(response.json()["message"])
                return
            else:
                print("Registration success! Hello {}!".format(id))
                self.session = response.json()["session"]
                self.user_id = response.json()["id"]
                self.manager_activity()

    def _client_login_flow(self) -> None:
        """Client Login Flow

        Includes ability to login as client and register new account.
        """
        print("=" * 10 + "Client Access" + "=" * 10)
        is_register = input("Do you have account? yes or no: ")
        # has an account, proceed to login
        if is_register == "yes":
            print("If this is your first time signing in, your password is the same as your name.\n")
            _id = input("id: ")
            pw = input("password: ")
            parameters = {"id": _id, "pw": pw, "_type": "client"}
            response = requests.post(f'{self.base_url}/v1/login/', params=parameters)
            if "message" in response.json().keys():
                print(response.json()["message"])
                return
            elif response.json()["active"] == 1:
                print("Login success! Hello {}".format(response.json()["user_id"]))
                self.session = response.json()["session"]
                self.user_id = response.json()["id"]
                self.client_activity()
            elif response.json()["active"] == 0:
                print("Client {} is deactivated. Contact the manager".format(_id))
                return
        # no account, proceed to register
        elif is_register == "no":
            name = input("What is your name? ")
            while True:
                client_email = input("What is your email address? ")
                if "@" in client_email:
                    break
                else:
                    print("Wrong email format")
            id = input("New username: ")
            pw = input("New password: ")
            parameters = {"name": name, "email": client_email, "id": id, "pw": pw, "_type": "client"}
            response = requests.post(f"{self.base_url}/v1/register/", params=parameters)
            print(response.json())
            if "message" in response.json().keys():
                print(response.json()["message"])
                return
            else:
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    subject = 'Welcome to the MPCS Labs Facility Management!'
                    body = "Hello {}!\n\nThis is a confirmation that you have successfully created an account for the MPCS Labs Facility Management system!".format(name)
                    message = "Subject: {}\n\n{}".format(subject, body)
                    smtp.sendmail(EMAIL_ADDRESS, client_email, message)
                print("Registration success! Hello {}! Your account confirmation have been sent to your email address.".format(id))
                self.session = response.json()["session"]
                self.user_id = response.json()["id"]
                self.client_activity()

    def program(self) -> None:
        """Base program
        
        Allows the swap between client and manager flows."""
        while True:
            if self.cli_login_active:
                res = input("1: facility manager, 2: client, 3: quit \n-> ")
            else:
                res = input("1: facility manager, 2: quit \n-> ")
            if res == "1":
                # manager flow
                self._manager_login_flow()
            elif res == "2":
                # client login disabled: quit
                if self.cli_login_active is False:
                    print("Program Exit")
                    return
                # client flow
                self._client_login_flow()
            elif res == "3":
                # client login enabled: quit
                print("Program Exit")
                return
            else:
                print("Please, type a number between 1 and 3 inclusive.")


if __name__ == "__main__":
    c = client(url='http://linux5.cs.uchicago.edu:51225').program()
    # deployed url:
    # http://linux5.cs.uchicago.edu
    