import sqlite3
import time
from database_functions import table_format, assign_trailers, new_trailer, login
from visualization_functions import (trailer_bar_chart, trailer_status_counts, carrier_load_counts,
                                     load_frequency_table, active_loads_summary)

# function to give the user options to navigate the database program
def main_menu(db_cursor):
    while True:
        print("\nPlease select from the following options (1-5):")
        print(" 1. View Planned Loads")
        print(" 2. View Trailers in Yard")
        print(" 3. View Active Loads")
        print(" 4. Check in a new trailer")
        print(" 5. Exit Program")

        option = input("Selection: ")

        if option == "1":
            # Query the info from the Planned Loads Table
            planned_loads_query = 'SELECT * FROM planned_loads'
            planned_loads_headers = ["Load ID", "Required Length (ft)", "Required Height (ft)", "Carrier Code",
                                     "Destination",
                                     "Special Requirements"]
            table_format(db_cursor, planned_loads_query, planned_loads_headers, "Planned Loads")

            # generate a frequency table for carrier loads
            carrier_counts = carrier_load_counts(db_cursor)
            load_frequency_table(carrier_counts)

        elif option == "2":
            # Query the info from the Trailers In Yard Table
            trailers_in_yard_query = 'SELECT * FROM trailers_in_yard'
            trailer_in_yard_headers = ["Trailer ID", "Trailer Number", "Length (ft)", "Height (ft)", "Carrier Code",
                                       "Availability", "Check In Date"]
            table_format(db_cursor, trailers_in_yard_query, trailer_in_yard_headers, "Trailers In Yard")

            # generate an ASCII bar chart for trailer availability
            status_counts = trailer_status_counts(db_cursor)
            trailer_bar_chart(status_counts)

        elif option == "3":
            # Query the info from the Active Loads Table
            active_loads_query = 'SELECT * FROM active_loads'
            active_loads_headers = ["Assignment ID", "Load ID", "Trailer ID", "Assignment Date"]
            table_format(db_cursor, active_loads_query, active_loads_headers, "Active Loads")

            active_loads_summary(db_cursor)

        elif option == "4":
            new_trailer(db_cursor, connection)
        elif option == "5":
            break
        else:
            print("Invalid option.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Establishes a connection to the database
    connection = sqlite3.connect('../Distribution Center BD.db')
    cursor = connection.cursor()

    while True:
        if login(cursor, connection):
            break

    time.sleep(1)
    print("Initializing...\n")
    time.sleep(2)

    # Test the connection with a basic query displaying all the available tables in the database
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table';")
    print("Tables in database:", cursor.fetchall())
    time.sleep(2)

    print("\nThe program will now check to see if any loads can be assigned a trailer")
    time.sleep(2)
    assign_trailers(cursor, connection)

    main_menu(cursor)

    print("\nThank you for taking the time to view the database.  Have a nice day.")
    connection.close()
