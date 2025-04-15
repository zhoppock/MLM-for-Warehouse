import time

# function to make a frequency table for the number of planned loads for each carrier
def load_frequency_table(data):
    print("\nFrequency Table of Planned Loads")
    print("Carrier Code | Count")
    print("-" * 20)
    for carrier, value in data.items():
        print(f"{carrier:12} | {value}")
    time.sleep(1)

# function to get numbers of all loads from the 'planned_loads' table, grouped by Carrier Code
def carrier_load_counts(cursor):
    cursor.execute("SELECT carrier_code, COUNT(*) AS Count "
                    "FROM planned_loads "
                    "GROUP BY carrier_code")
    results = cursor.fetchall()

    # convert results to a dictionary and return the results immediately
    return {row[0]: row[1] for row in results}

# function to make an ASCII bar chart visualizing the number of "available" trailers vs "assigned" trailers
def trailer_bar_chart(data):
    print("\nChart of Trailer Statuses")
    max_count = max(data.values())
    for status, count in data.items():
        bar = "#" * int((count / max_count) * 50)  # scale bars to fit 50 characters
        print(f"{status.upper()}: {bar} ({count})")
    time.sleep(1)

# function to get numbers of all trailers from the 'trailers_in_yard' table, grouped by Availability
def trailer_status_counts(cursor):
    cursor.execute("SELECT availability, COUNT(*) AS Count "
                    "FROM trailers_in_yard "
                    "GROUP BY availability")
    results = cursor.fetchall()

    # convert results to a dictionary and return the results immediately
    return {row[0]: row[1] for row in results}

# function to display a textual summary of active loads
def active_loads_summary(cursor):
    # Sample data returned from the SQL query (Replace this with your actual query result)
    cursor.execute("SELECT trailers_in_yard.carrier_code, trailers_in_yard.trailer_number "
                    "FROM active_loads "
                    "JOIN trailers_in_yard ON active_loads.trailer_id = trailers_in_yard.trailer_id ")
    results = cursor.fetchall()

    # create a dictionary to hold the grouped data
    carrier_trailers = {}

    # process the query result to group trailers by carrier
    for carrier, trailer in results:
        if carrier not in carrier_trailers:
            carrier_trailers[carrier] = []
        carrier_trailers[carrier].append(trailer)

    # display the results in a text-based format
    print("\nActive Loads Grouped by Carrier:\n")
    for carrier, trailers in carrier_trailers.items():
        print(f"Carrier: {carrier}")
        print(f"  Assigned Trailers: {', '.join(trailers)}\n")
    time.sleep(1)