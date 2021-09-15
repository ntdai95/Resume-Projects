from uuid import uuid4
from fastapi import FastAPI
from typing import Optional, Union, Dict, Any
from pydantic import BaseSettings, BaseModel
from datetime import datetime, timezone, timedelta
from pydantic.types import Json
import reservation
import json
import random
import hashlib


global client_login, manager_registration, environment


class Settings(BaseSettings):
    """
    Base database settings
    """
    database: str = "reservation_system"

class Hold(BaseModel):
    """Hold class

    The agreed upon class for the hold interoperability.
    """
    username: str 
    password: str
    client_name: str
    request: str
    start_date: str #YYYY-MM-DD
    start_time: str
    end_time: str

#######################
#   Startup actions   #
#######################

settings = Settings()
app = FastAPI()
db = reservation.Database(settings.database)
program = reservation.Program(db)
client_login = 0
manager_registration = 0
environment = "prod"
sessions = {}   # session hash : [last action, user_type]


def _load_config():
    """Load config

    Loads the config options on startup.
    """
    global client_login, manager_registration, environment
    with open('config.json') as config_file:
        config = json.load(config_file)
        client_login = config['options']['client_login']
        manager_registration = config['options']['manager_registration']
        environment = config['environment']

_load_config()

# Database protections
if environment != "prod":
    if settings.database == "reservation_system":
        raise EnvironmentError("Production database outside of production environment.")

#######################
# Internal functions  #
#######################

def _validate_datetime(date: str, time: str = "00:00", check_in_past=False) -> Union[dict, bool]:
    """Validate datetime
    
    Validate if date and time provided are good dates and in the future.

    Args:
        date: a string in the format YYYY-MM-DD or YYYY-M-D or using /
    Returns:
        True: date and time or just date are valid and in the future.
        False: date or time are not valid or in the past.
    """
    try:
        date = date.replace('/', '-')
        dt = datetime.strptime((date + " " + time), '%Y-%m-%d %H:%M')
        # convert all times to CDT (-6)
        dt = dt.astimezone(timezone(-timedelta(hours=6)))
        now = datetime.now(timezone(-timedelta(hours=6))).astimezone()
        if dt < now and check_in_past:
            return {"message": "This date or time is in the past."}
        return True
    except ValueError:
        return {"message": "This is not a valid date or time format. Required:  YYYY/MM/DD"}

def _validate_session(session: str, action_level: str = '') -> bool:
    """Validate session
    
    Validate a session action exists, hasn't expired, and has the priveleges
    for the requested action. When valid, the session time is reset to now.

    Args:
        session: a string with a uuid4
        action_level: client or manager
    Returns:
        True: has the privelege and isn't expired
        False: no session, expired session, or no privelege
    """
    if session in sessions:
        if sessions[session][0] < datetime.today() - timedelta(hours=1):
            # expired
            sessions.pop(session)
            return False
        elif action_level:
            if action_level != sessions[session][1]:
                # no permission
                return False
            else:
                sessions[session][0] = datetime.today()
                return True
        else: 
            sessions[session][0] = datetime.today()
            return True
    else:
        # no session
        return False

#######################
#   Basic endpoints   #
#######################

@app.get("/")
async def root():
    return {"message": "You must use /v1/"}

@app.get("/v1")
async def root_v1(session: Optional[str] = ''):
    """Root v1

    Returns simple json unless provided a valid manager session, then it return environment,
    client login, and session info.
    """
    global client_login, environment
    if session:
        if session in sessions:
            active_sessions = len(sessions)
            return {"message": "Reservation System Root V1", 
                    "Environment": environment, 
                    "Client_Login": client_login,
                    "Active": active_sessions}
    return {"message": "Reservation System Root V1"}

@app.get("/v1/login_status/")
async def login_status():
    """Login status

    Returns:
        if client_login is enabled or disabled
    """
    global client_login
    return {"client_login": client_login}

#######################
#    Hold endpoints   #
#######################

@app.post("/hold")
async def hold_post(hold: Hold):
    """Hold post

    Add a hold to database.

    Args:
        hold: the hold criteria
    Returns:
        json with success and facility info
    """
    args = hold.dict()
    if args['request'].startswith("workshop"):
        request = args['request']
    elif args['request'] == "polymer extruder1":
        request = "extrud1"
    elif args['request'] == "polymer extruder2":
        request = "extrud2"
    elif args['request'] == "high velocity crusher":
        request = "crusher"
    elif args['request'] == "mini microvac1":
        request = "microv1"
    elif args['request'] == "mini microvac2":
        request = "microv2"
    elif args['request'] == "1.21 gigawatt lightning harvester":
        request = "harvest"
    elif args['request'] == "irradiator1":
        request = "irrad1"
    elif args['request'] == "irradiator2":
        request = "irrad2"
    else:
        message = "Please, type one of the following exactly as it is: workshop1, workshop2, " \
                  "workshop3, workshop4, polymer extruder1, polymer extruder2, high velocity " \
                  "crusher, mini microvac1, mini microvac2, 1.21 gigawatt lightning harvester, " \
                  "irradiator1, irradiator2."
        return {"success": False, "message": message, "facility_name": "APIGROUP5 at Chicago, IL"}

    pwh = hashlib.sha256(args['password'].encode()).hexdigest()
    user = db.login(args['username'], pwh, "manager")
    if not user:
        return {"success": False, "message": "Invalid id/password", "facility_name": "APIGROUP5 at Chicago, IL"}

    client_list = db.find_exact_client(args['client_name'])
    if client_list == []: # Adding a new customer if no such client is found
        customer_id = db.add_user(args['client_name'], 'client')
    else:
        customer_id = client_list[0][0]

    # Try making reservation:
    if (check := _validate_datetime(args['start_date'], args['start_time'], True)) != True:
        reservation_result = check
    if request.startswith("workshop"):
        request = request[8:]  # Only need the workshop number
        if int(request) > 4 or int(request) < 1:
            reservation_result = {"message": "That workshop does not exist."}
        else:
            reservation_result = program.make_workshop_reservation(request,
                                                                   customer_id,
                                                                   args['start_date'],
                                                                   args['start_time'],
                                                                   args['end_time'])
            if "message" in reservation_result.keys():
                return {"success": False, "message": reservation_result["message"], "facility_name": "APIGROUP5 at Chicago, IL"}
            else:
                db.add_hold_status_to_reservation(args['client_name'], reservation_result['reservation_id'])
    elif request not in {'microv1', 'microv2', 'irrad1', 'irrad2',
                         'extrud1', 'extrud2', 'harvest', 'crusher'}:
        reservation_result = {"message": "That machine does not exist."}
    else:
        reservation_result = program.make_machine_reservation(request,
                                                              customer_id,
                                                              args['start_date'],
                                                              args['start_time'],
                                                              args['end_time'])
        if "message" in reservation_result.keys():
            return {"success": False, "message": reservation_result["message"], "facility_name": "APIGROUP5 at Chicago, IL"}
        else:
            db.add_hold_status_to_reservation(args['client_name'], reservation_result['reservation_id'])

    message = "Reservation success!\n" + "=" * 40 + \
              "\nReservation Info\nreservation id: {}\n".format(reservation_result['reservation_id']) + \
              "total cost: {}".format(reservation_result['total_cost'])
    return {"success": True, "message": message, "facility_name": "APIGROUP5 at Chicago, IL"}

@app.get("/hold")
async def hold_get():
    """Hold get

    Get all holds.
    """
    hold_reservation_list = db.get_hold_reservations()
    return json.dumps([(row) for row in hold_reservation_list])

#########################
# Reservation endpoints #
#########################

@app.get("/v1/reservations/")
async def reservation_get(start: str, end: str, session: str, customer_id: Optional[str] = None):
    """Get a reservation

    Get reservations based on matching criteria.

    Args:
        start: starting datetime
        end: ending datetime
        session: the user session
        customer_id: the customer id for reservations
    Returns:
        a json with error or the reservation rows
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    if (check := _validate_datetime(start)) != True:
        return check
    elif (check := _validate_datetime(end)) != True:
        return check
    start = start.replace('/', '-')
    end = end.replace('/', '-')
    if not customer_id:
        reservation_list = db.get_reservations(start, end)
    else:
        reservation_list = db.get_reservations(start, end, int(customer_id))
    if reservation_list == []:
        return {"message": "We did not find any reservations with those details."}
    return json.dumps([(row) for row in reservation_list])

@app.get("/v1/reservations/{reservation_id}")
async def single_reservation_get(reservation_id: str, session: str):
    """Get a reservation

    Get a single reservation based on the reservation id.

    Args:
        reservation_id: the reservation_id uuid
        session: the logged in session
    Returns:
        json of reservation rows
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    reservation_list = db.get_reservation_by_id(reservation_id)
    if reservation_list == []:
        return {"message": "We did not find any reservations with those details."}
    return json.dumps([(row) for row in reservation_list])


@app.post("/v1/reservations/")
async def reservation_post(
        customer_id: str,
        reservation_date: str,
        thing_to_reserve: str,
        start_time: str,
        end_time: str,
        session: str) -> Json:
    """Reservation post

    Make a reservation in the database.

    Args:
        customer_id: the customer id for the reservation
        reservation_date: the date of the reservation
        thing_to_reserve: the thing to reserve in the reservation
        start_time: the starting reservation time
        end_time: the ending reservation time
        session: the logged in user session
    Returns:
        json results or message for error
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    if (check := _validate_datetime(reservation_date, start_time, True)) != True:
        return check
    reservation_date = reservation_date.replace('/', '-')
    if thing_to_reserve.startswith("workshop"):
        thing_to_reserve = thing_to_reserve[8:]  # Only need the workshop number
        if int(thing_to_reserve) > 4 or int(thing_to_reserve) < 1:
            return {"message": "That workshop does not exist."}
        result = program.make_workshop_reservation(
            thing_to_reserve,
            customer_id,
            reservation_date,
            start_time,
            end_time
        )
    else:
        if thing_to_reserve not in {
            'microv1',
            'microv2',
            'irrad1',
            'irrad2',
            'extrud1',
            'extrud2',
            'harvest',
            'crusher'}:
            return {"message": "That machine does not exist."}
        result = program.make_machine_reservation(
            thing_to_reserve,
            customer_id,
            reservation_date,
            start_time,
            end_time
        )
    return result

@app.delete("/v1/reservations/")
async def reservation_delete(reservation_id: str, session: str) -> Dict[str, Any]:
    """Delete a reservation

    Args:
        reservation_id: specific reservation id
        session: logged in session hash
    Returns:
        message of success or error
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    result = program.cancel_reservation(reservation_id)
    return result

#########################
# Transaction endpoints #
#########################

@app.get("/v1/transactions/")
async def get_transaction(start: str, end: str, session: str, customer_id: Optional[str] = None):
    """Get a transaction

    Args:
        start: start datetime
        end: end datetime
        session: logged in session hash
        customer_id (opt): specific customer id to narrow results
    Returns:
        Matching transactions
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    if (check := _validate_datetime(start)) != True:
        return check
    elif (check := _validate_datetime(end)) != True:
        return check
    start = start.replace('/', '-')
    end = end.replace('/', '-')
    transaction_list = db.get_all_transactions(start, end, customer_id)
    if transaction_list == []:
        return {"message": "We did not find any transactions with those details."}
    return json.dumps([(row) for row in transaction_list])

#########################
#  User acct endpoints  #
#########################

@app.post("/v1/clients/")
async def add_customer(name: str, session: str):
    """Add a customer

    Args:
        name: customer name
        session: logged in session hash
    Returns:
        customer id: id for the customer
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    customer_id = db.add_user(name, 'client')
    return {"customer_id": customer_id}

@app.post("/v1/register/")
async def register(name: str, email: str, id: str, pw: str, _type: str):
    """Register endpoint for only clients.

    Args:
        name: client name
        email: client email
        id: client login user id
        pw: client password (not encrypted)
        _type: client
    Returns:
        id: customer id
        session: session hash for this login
    """
    if _type == "manager":
        return {"message": "Must use manager registration."}
    pwh = hashlib.sha256(pw.encode()).hexdigest()
    customer_id = db.register(name, email, id, pwh, _type)
    if customer_id:
        session_hash = str(uuid4())
        sessions[session_hash] = [datetime.today(), _type]
        return {"id": customer_id, "session": session_hash}
    else:
        return {"message": "Already in use"}

@app.post("/v1/register_manager/")
async def register_manager(name: str, id: str, pw: str, _type: str):
    global manager_registration
    """Register endpoint for only managers.

    Args:
        name: manager name
        id: manager login id
        pw: manager password (not encrypted)
        _type: manager
    Returns:
        id: manager_id
        session: session hash for this login
    """
    if _type not in ['manager', 'client']:
        return {"message": "Not a proper type"}
    if manager_registration == 0:
        return {"message": "Manager registration not allowed."}
    pwh = hashlib.sha256(pw.encode()).hexdigest()
    manager_id = db.register(name, None, id, pwh, _type)
    if manager_id:
        session_hash = str(uuid4())
        sessions[session_hash] = [datetime.today(), _type]
        return {"id": manager_id, "session": session_hash}
    else:
        return {"message": "Already in use"}

@app.post("/v1/login/")
async def login(id: str, pw: str, _type: str):
    global client_login
    """Login endpoint for both client and manager

    Args:
        id: login user id
        pw: user password
        _type: client or manager
    Returns:
        id: client/manager id
        user_id: logged in id
        active: if user is active
        session: session hash to use for auth
    """
    if client_login == 0 and _type == "client":
        return {"message": "Client login not allowed."}
    pwh = hashlib.sha256(pw.encode()).hexdigest()
    login_user = db.login(id, pwh, _type)
    if login_user:
        session_hash = str(uuid4())
        sessions[session_hash] = [datetime.today(), _type]
        return {
            "id": login_user[0], 
            "user_id": login_user[1],
            "active": login_user[4],
            "session": session_hash}
    else:
        return {"message": "Invalid id/password"}

@app.post("/v1/user/update_password")
async def update_password(user_id: str, new_pw: str, session: str):
    """Update password endpoint

    Args:
        user_id: login user id
        new_pw: new password to change to
        session: logged in session hash
    Returns:
        message: success or error
    """
    if not _validate_session(session) and session != "Session Override":
        return {"message": "Logout and log back in."}
    pwh = hashlib.sha256(new_pw.encode()).hexdigest()
    result = db.update_password(user_id, pwh)
    if result:
        return {"message": "Password change successful", "success": 1}
    else:
        return {"message": "Something went wrong, try again"}

@app.post("/v1/client_login/")
async def client_login_change(new_status: int, session: str):
    """Client login change

    Changes the status of client login between enabled or disabled.

    Args:
        new_status: the new status to set
        session: the logged in user session
    Returns:
        message or current status
    """
    global client_login
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    client_login = new_status
    return {"client_login": client_login}

@app.get("/v1/user/")
async def get_user(user_id: str, session: str):
    """Get user
    
    Get a user's info based on their user_id.

    Args:
        user_id: the user_id to get info on
        session: the logged in user session
    Returns:
        json with the user info
    """
    if not _validate_session(session) and session != "Session Override":
        return {"message": "Logout and log back in."}
    user = db.get_user(user_id)
    return user

@app.get("/v1/clients/")
async def get_clients(session: str):
    """Get client list

    Args: 
        session: logged in session hash
    Returns:
        List of all clients
    """
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    client_list = db.get_clients()
    if client_list == []:
        return {"message": "We have no clients."}
    return json.dumps([(row) for row in client_list])

@app.post("/v1/find_client/")
async def find_client(pname: str, session: str):
    """Search for a client

    Args:
        pname: partial name to search
        session: logged in session hash
    Returns:
        client list or message for error
    """
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    client_list = db.find_client(pname)
    if client_list == []:
        return {"message": "We have no clients with that partial name."}
    return json.dumps([(row) for row in client_list])

@app.post("/v1/activate/")
async def activate_client(user_id: str, session: str):
    """Activate client

    Activates a specific client to being able to login.

    Args:
        user_id: the user id to activate
        session: the logged in user session
    Returns:
        json with message for error or the user_id
    """
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    user_id = db.set_client_activeness(user_id, 1)
    if user_id:
        return {"user_id": user_id}
    else:
        return {"message": "Invalid client id"}

@app.post("/v1/deactivate/")
async def deactivate_client(user_id: str, session: str):
    """Deactivate client

    Deactivates a specific client from being able to login.

    Args:
        user_id: the user id to deactivate
        session: the logged in user session
    Returns:
        json with message for error or the user_id
    """
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    user_id = db.set_client_activeness(user_id, 0)
    if user_id:
        return {"user_id": user_id}
    else:
        return {"message": "Invalid client id"}

@app.get("/v1/funds")
async def get_funds(user_id: str, session: str):
    """Get funds

    Get funds for a user.

    Args:
        user_id: the user id to get funds for
        session: the logged in user session
    Returns:
        json with user_id and balance
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    user_funds = db.get_user_funds(user_id)
    user_funds = float("{:.2f}".format(user_funds))
    return {"user": user_id, "account_balance": user_funds}

@app.post("/v1/funds")
async def post_funds(user_id: str, amount: str, session: str):
    """Post funds

    Add or take away funds from a user's account.

    Args:
        user_id: the user_id to change funds on
        amount: the amount to change by (can be negative for subtracting)
        session: the logged in user session'
    Returns:
        a json with message for error or the user_id and balance
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    user_funds = db.post_user_funds(user_id, amount)
    if user_funds is False:
        amount = db.get_user_funds(user_id)
        return {"message": "You do not have enough money to make this transaction", 
                "user": user_id, "account_balance": amount}
    user_funds = float("{:.2f}".format(user_funds))
    return {"user": user_id, "account_balance": user_funds}

#########################
#   History endpoints   #
#########################

@app.get("/v1/report_history/")
async def get_report_history(id: int, search_type: str, session: str):
    """Get report history

    Gets the report history.

    Args:
        id: the id for the search
        search_type: the type of search
        session: the logged in user session
    Returns:
        json of the report history
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    history = db.get_report_history(id, search_type)
    return json.dumps([row for row in history])

@app.post("/v1/report_history/")
async def add_report_history(
        id: int, 
        search_id: str, 
        search_start: datetime, 
        search_end: datetime, 
        search_type: str, 
        session: str):
    """Add report history

    Adds reports to the history.

    Args:
        id: the user_id
        search_id: the id of the search
        search_start: the start of the search
        search_end: the end of the search
        search_type: the type of search
        session: the logged in user session
    Returns:
        json with message for error or an id for the added log
    """
    if not _validate_session(session):
        return {"message": "Logout and log back in."}
    print("added report history")
    log = db.add_report_history(id, search_id, search_start, search_end, search_type)
    return {"id": log["id"]}

#########################
#    Admin endpoints    #
#########################

@app.get("/v1/reset_app/")
async def reset_app(password_hexdigest: str, session: str) -> Dict[str, str]:
    """Reset app
    
    Reset the production database to a clean state

    Args:
        password_hexdigest: the hex of the password to enable reset
        session: the logged in user session
    Returns:
        json with reset complete message
    """
    global environment
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    if environment == "prod":
        return {"message": "Method not allowed in production."}
    hex_digest = '9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c'
    if password_hexdigest == hex_digest:
        db.create_tables(db.conn, drop="apigroup5 please drop")
        print("reset successful")
        return {"message": "Reset complete."}
    else:
        # we always return the same thing regardless of success
        print("reset attempted: failed")
        return {"message": "Reset failed."}

@app.get("/v1/load_db/")
async def load_db(password_hexdigest: str, session: str) -> Dict[str, str]:
    """Load db

    Fill the database with some random users and reservations. Likely that some will conflict.

    Args:
        password_hexdigest: the hexdigest of password
        session: the logged in user session
    Returns:
        json with success or fail message
    """
    global environment
    if not _validate_session(session, 'manager'):
        return {"message": "Logout and log back in."}
    if environment == "prod":
        return {"message": "Method not allowed in production."}
    hex_digest = '9f17371c0be6c2acd47bc433091d420c47060e78ba83eb2e4980c0cb1eb7288c'
    if password_hexdigest == hex_digest:
        names = []
        for i in range(10):
            names.append(f'TestName{i}')
        customer_ids = []
        dates = ['2021-6-14', '2021-6-15', '2021-6-16']
        things_to_reserve = ['microv1', 'microv2', 'irrad1', 'irrad2', 'workshop1', 'workshop2']
        start_times = ['10:00', '10:30' '11:00', '11:30']
        end_times = ['12:00', '13:00', '14:00']
        for name in names:
            customer_ids.append(program.db.add_user(name, 'client'))
        for customer_id in customer_ids:
            for date in dates:
                await reservation_post(
                    customer_id,
                    date,
                    random.choice(things_to_reserve),
                    random.choice(start_times),
                    random.choice(end_times),
                    session)
        return {"message": "Data added for dates 2021/6/14 - 2021/6/16."}
    else:
        return {"message": "Operation failed."}
