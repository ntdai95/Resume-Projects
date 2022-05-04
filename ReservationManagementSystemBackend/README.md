***Note: You need to create a .env file with EMAIL_ADDRESS=<app_email_address_as_string> and EMAIL_PASSWORD=<app_email_password_as_string> environment variables.***

# Install Requirements:
Type the following command to installed the required python modules: pip3 install -r requirements.txt

# How To Run The Program Remotely

The reservation server is currently running on the U Chicago Linux server #5. To use the reservation client, all you need to do is run the client program locally with the following command:\
**python client.py**

Peter and Spencer both have logins as facility managers with the following credentials:\
name: peter\
password: peter

name: spencer\
password: spencer

If you would like to test the program with a local instance of the server, you can remove the explicit url in this line of client.py:\
c = client(url='http://linux5.cs.uchicago.edu:51225').program()

Then, you simply need to start the server locally with the following bash command:\
uvicorn main:app --reload --host 0.0.0.0 --port 51225

Then start the client with:\
python client.py


# How To Run The Tests
Navigate to the root directory, and then type:

**Running Specific Tests**
pytest tests\test_database.py \
pytest tests\test_main.py     \
pytest tests\test_reservation.py

**Running All Tests**
pytest


# TA-05 Program Description

**Our Facility**

Our facility is located in the beautiful city of Chicago, IL. We operate in Central Time and are open from 9am to 6pm on weekdays and from 10am to 4pm on Saturdays. \
We are closed on Sundays.

**Program Overview**

Our main program is a persistent command line program that allows facility managers and clients to access a dashboard, filled with options of what they can do within our facility. Facility managers have different options than clients, and client logins need to be enabled (at least once) by a facility manager. After client login is enabled, client users can access the program directly and choose from a wide variety of options.

When you start the program, it will pull the current status of the client login feature. If it had been set previously, then you won't need to log in as a facility manager to enable it. If it had not been set previously, then the user will need to log in first as a facility manager.

Users cannot make reservations in the past, or make reservations for days where the thing to reserve is already reserved. Users also cannot make reservations for which they do not have the funds to cover the total cost of the reservation (even if the client's funds are able to pay for the down payment).

If the reservation requested is invalid, the user will see that information and can then make a different request.

**Making a Reservation (Interoperability)**

When a user makes a reservation, it will first check our local facility to see if this machine is available at this time. If it is not, but the reservation is otherwise valid, the program will randomly shuffle through the other four locations and try to make the reservation with their machine at the specified time. The program will randomly shuffle through until it finds an open machine, or until it has gone through all four other locations.

If none of the locations have this machine available, the user will be alerted and offered to choose another time for their reservation.

**Manager Dashboard**\
As a manager, you have the ability to do any of the following tasks:

- 1  = Activate client login
- 2  = Deactivate client login
- 3  = Activate client
- 4  = Deactivate client
- 5  = Get Client Reservation Report
- 6  = Edit a reservation
- 7  = Cancel a reservation
- 8  = List all clients
- 9  = Get all reservations
- 10 = Create new customer
- 11 = Edit customer account
- 12 = Find client account
- 13 = Transaction Reports
- 14 = Manager Dashboard
- logout = logout

Before any clients can log in, a manager has to enable the ability to allow client logins. This is a persistent feature flag so that even after a facility manager logs out, clients will still be able to log in.
For the privacy of the users, managers cannot alter client login details like user_id or password. If managers choose to "edit a customer account", they can choose to add funds to the account. 

Managers can do all similar things to clients except make a new reservation. They can also return reports either for all users or single clients. Managers can also deactivate specific user accounts from being able to login. The manager dashboard will display the status of client logins, which enviornment the program is running in, and how many active sessions there are currently.

**Client Dashboard**\
Once client logins are enabled, a logged-in client will have the option to do any of the following things. Once logins are enabled, clients can also register themselves for a client account.
- 1 = List my reservations
- 2 = Edit a reservation
- 3 = Make a reservation
- 4 = Cancel a reservation
- 5 = Add funds to my account
- 6 = List my transactions
- 7 = Edit my profile 
- 8 = Show my account balance 
- logout = logout

When they choose to list reservations or transactions, clients will see all of the relevant data related to their own actions. They can also add funds to their account if they are running low, or query their account balance. 
Every new client starts off with $10,000 in funds.
Clients can also make changes to their account from their dashboard. They can cancel a reservation, edit a reservation's dates or times, or change their own password.

When a new client account is created, an email is sent to the registered email confirming their account.


# Other Design Decisions (Optional Features)

**Security - Session Updates**\
When a user logs in or registers (which logs you in by default), the server stores a token of your privileges and the current time. The server then returns that session ID back to the client. Client-side, that session ID is stored locally and whenever the user makes any request to the server, the session ID is sent along with the request. 

The server requires a valid session token for any request. A valid session token:
- 1. exists
- 2. has to have been refreshed within the last hour
- 3. shows that this user has the permissions to do what they are requesting

Whenever a session is validated, the server will refresh the time stored in the session token to the time of the last action.

This session token also prevents remote facility managers from making any changes in our system. This is becasue while the hold endpoint requires a login and password, is the only endpoint that does not return a session. Therefore, even though remote facility managers can make holds, they cannot make any other changes or get any other information.

**Saved Reports**\
These features give the user the option to manually write the date interval from which they want to display the information, or choose from previous search parameters for the same reports (mainly date and id).

Available for Managers for following options: 
- option 5 (Get client reservation report)
- option 9 (Get all reservations)
- option 13 (Get transaction reports)

Available for Clients for following options: 
- option 1 (list my reservations)
- option 3 (make reservation)
- option 6 (list my transactions)

**Export Report (csv format)**\
After running any of the follow reports users can choose to save the report in a csv file.

Available for Managers for following options: 
- option 5 (Get client reservation report)
- option 8 (List all Clients) 
- option 9 (Get all reservations)
- option 13 (Get transaction reports)

Available for Clients for following options: 
- option 1 (list my reservations)
- option 3 (make reservation)
- option 6 (list my transactions)

**Finding Clients**\
Facility managers can search for users using the first letter (or few letters) of a client's name. This will return information like the client's ID number, username, and first name.

# API Documentation

Documentation can be found at the link here: [http://linux5.cs.uchicago.edu:51225/docs](http://linux5.cs.uchicago.edu:51225/docs)
