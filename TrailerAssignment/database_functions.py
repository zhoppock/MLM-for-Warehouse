# external library that can be used to delay the program
import time
# external library that can populate SQLite data in a table format
from tabulate import tabulate


# function to authenticate a user to enter the database program
def login(cursor, connection):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # query database to check if a user exists with the entered credentials
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()  # grabs the first match

    if user:
        print(f"\nHello {username}, and welcome to the Distribution Center Database.\n")
        connection.commit()
        return True  # successful login
    else:
        print(" > Invalid username or password. Please try again.")
        return False  # failed login


# function to format the data in a database table into a Python grid
def table_format(cursor, query, headers, table_name):
    # Query the info from the designated table
    cursor.execute(query)
    rows = cursor.fetchall()
    # Format and display the results of the designated table in a grid format
    print(f"\n{table_name}:")
    print(tabulate(rows, headers=headers, tablefmt='grid'))
    time.sleep(2)


# function to pull a list of available trailers
def fetch_trailers(cursor):
    cursor.execute("SELECT * FROM trailers_in_yard "
                   "WHERE availability = 'available'")
    available_trailers = cursor.fetchall()
    return available_trailers


# function to assign available trailers to loads as long as they match specific parameters
def assign_trailers(cursor, connection):
    # pull planned loads
    cursor.execute("SELECT * FROM planned_loads "
                   "WHERE load_id "
                   "NOT IN (SELECT load_id FROM active_loads)")
    unassigned_loads = cursor.fetchall()
    count = 0

    for load in unassigned_loads:
        (load_id, required_length, required_height, carrier_code, destination, special_requirements) = load

        # Find matching trailer by pulling available trailers
        for trailer in fetch_trailers(cursor):
            (trailer_id, trailer_number, trailer_length, trailer_height, trailer_carrier_code, availability,
             check_in_date) = trailer
            if (trailer_length == required_length and trailer_height == required_height
                    and trailer_carrier_code == carrier_code):
                print(f" > Assigning trailer {trailer_number} to load {load_id}")
                time.sleep(1)

                # Update trailer availability in the trailers_in_yard table
                cursor.execute("UPDATE trailers_in_yard "
                               "SET availability = 'assigned' "
                               "WHERE trailer_id = ?",
                               (trailer_id,))

                # Insert the assignment into the active_loads table
                cursor.execute("INSERT INTO active_loads (load_id, trailer_id) "
                               "VALUES (?, ?)", (load_id, trailer_id))

                # Commit the changes
                connection.commit()
                count += 1
                break
    print(f"\n{count} load(s) were assigned a trailer")
    time.sleep(2)


# function to check in a new trailer into the database
def new_trailer(cursor, connection):
    print("\n")
    # start by entering a trailer number.  There is a check to make sure no duplicates are entered in
    while True:
        trailer_number = input("Please enter a trailer number: ")
        if trailer_number:
            cursor.execute("SELECT * FROM trailers_in_yard "
                           "WHERE trailer_number = ?",
                           (trailer_number,))
            existing_trailer = cursor.fetchone()
            if existing_trailer:
                print(f" > Trailer number {trailer_number} already exists in the system.")
            else:
                break
        else:
            print(" > You cannot leave this section blank.")

    # next, enter the trailer's length.  There is a check to make sure the input should only be either 48 or 53
    while True:
        try:
            trailer_length = int(input("Please enter the trailer length (either 48 or 53, in feet): "))
            if trailer_length in (48, 53):
                break
            else:
                print(" > Length must be either 48 or 53, in feet.")
        except ValueError:
            print(" > Entry must be valid.")

    # next, enter the trailer's height.  There is a check to make sure the input should only be either 12 or 14
    while True:
        try:
            trailer_height = int(input("Please enter the trailer height (either 12 or 14, in feet): "))
            if trailer_height in (12, 14):
                break
            else:
                print(" > Height must be either 12 or 14, in feet.")
        except ValueError:
            print(" > Entry must be valid.")

    # finally, enter the trailer's Carrier code.  There is a check to make sure the code is 4 or fewer characters
    while True:
        carrier_code = input("Please enter the Carrier code (must be 4 characters or fewer): ").strip().upper()
        if 4 >= len(carrier_code) > 0:
            break
        elif len(carrier_code) > 4:
            print(" > Carrier code must be 4 characters or fewer.")
        else:
            print(" > You cannot leave this section blank.")

    # the trailer details will now be put into the trailers_in_yard table
    cursor.execute("INSERT INTO trailers_in_yard (trailer_number, trailer_length, trailer_height, carrier_code)"
                   "VALUES (?, ?, ?, ?)",
                   (trailer_number, trailer_length, trailer_height, carrier_code))
    connection.commit()
    print(f"\nTrailer {trailer_number} successfully entered into the database.")

    print("\nChecking if trailer can be assigned to a load.")
    time.sleep(2)
    assign_trailers(cursor, connection)
