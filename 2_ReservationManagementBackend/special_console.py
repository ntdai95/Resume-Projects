import requests


class SpecialClient:
    """Send a hold request

    Sending a hold request to the any of the 5 facilities in the system. User can specify whether he/she
    wants to select a specific facility to send a hold request or to let the program randomly choose it.
    It will keep asking and try to send request to the other facilities until all the 5 facilities have
    rejected the hold request or one of the facilities has accepted it.
    """
    def __init__(self, url: str = 'http://localhost:51225'):
        """Init method

        Args:
            url: the base url that the server is located at with port
        """
        self.base_url = url
        self.things = {"microv1", "microv2", "irrad1", "irrad2", "extrud1", "extrud2", "crusher", 
                       "harvest", "workshop1", "workshop2", "workshop3", "workshop4"}
        self.dictionary = {}


    def program(self) -> None:
        """
        Base program

        It allows the user to test out sending hold requests (specific or random) to 
        different facilities and see their returning responses.
        """
        self.dictionary['username'] = input("Enter your username (if you are spencer or peter, type spencer or peter): ")
        self.dictionary['password'] = input("Enter your password (if you are spencer or peter, type spencer or peter): ")
        self.dictionary['client_name'] = input("Enter the name of the client that you want to make a request for: ")
        print("Make a Hold Request")
        print("=" * 40)

        while True:
            thing_to_reserve = input("What do you want to reserve? \n"
                "(options: \n\tmicrov1(2,000/hr), \n\tmicrov2(2,000/hr), \n\tirrad1(2,200/hr), "
                "\n\tirrad2(2,200/hr), \n\textrud1(500/hr), \n\textrud2(500/hr), \n\tcrusher(20,000/hr), "
                "\n\tharvest(8,800/hr), \n\tworkshop1(99/hr), \n\tworkshop2(99/hr), "
                "\n\tworkshop3(99/hr),\n\tworkshop4(99/hr)) \n->")
            if thing_to_reserve in self.things:
                break
            print("Our facility only has the following equipments/workshops: "
                  "microv1, microv2, irrad1, irrad2, extrud1, extrud2, "
                  "crusher, harvest, workshop1, workshop2, workshop3, or workshop4")

        while True:
            self.dictionary['start_date'] = input("\nWhat date do you want to do your reservation? (yyyy-mm-dd, "
                                                  "Our facility does not support recurring reservations.)\n -->")
            self.dictionary['start_time'] = input("What time do you want to start the reservation? (HH:MM)\n --> ")
            self.dictionary['end_time'] = input("What time do you want to end the reservation? (HH:MM, inclusive; "
                                                "min. 1 hour; please enter a time range within normal business "
                                                "hours)\n --> ")
            # standardizing item request to match facility 5's formats
            if thing_to_reserve == "extrud1":
                self.dictionary['request'] = "polymer extruder1"
            elif thing_to_reserve == "extrud2":
                self.dictionary['request'] = "polymer extruder2"
            elif thing_to_reserve == "crusher":
                self.dictionary['request'] = "high velocity crusher"
            elif thing_to_reserve == "microv1":
                self.dictionary['request'] = "mini microvac1"
            elif thing_to_reserve == "microv2":
                self.dictionary['request'] = "mini microvac2"
            elif thing_to_reserve == "harvest":
                self.dictionary['request'] = "1.21 gigawatt lightning harvester"
            elif thing_to_reserve == "irrad1":
                self.dictionary['request'] = "irradiator1"
            elif thing_to_reserve == "irrad2":
                self.dictionary['request'] = "irradiator2"

            try:                    
                if self.base_url == "http://localhost:51225":
                    response = requests.post('{}/hold'.format(self.base_url), json=self.dictionary)
                    json_object_reservation_other_facility = response.json()
                else:
                    response = requests.post('http://linux5.cs.uchicago.edu:51225/hold', json=self.dictionary)
                
                json_object_reservation_other_facility = response.json()
                if json_object_reservation_other_facility["success"]:
                    print("\nYour reservation has been scheduled at " + json_object_reservation_other_facility["facility_name"])
                    print("=" * 40)
                    print(json_object_reservation_other_facility["message"])
                else:
                    print("\n" + json_object_reservation_other_facility["message"])
                    print("=" * 40)
                    print("Unfortunately, the {} facility cannot accomodate your reservation at this time.".format(json_object_reservation_other_facility['facility_name']))

                break
            except:
                pass
            
        print("Goodbye!")


if __name__ == "__main__":
    SpecialClient(url='http://linux5.cs.uchicago.edu:51225').program()