import pyodbc

# List all available ODBC drivers on your system
# drivers = [driver for driver in pyodbc.drivers()]
# print(drivers)
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://docs.healtheintent.com/feed_types/millennium-ods/v1/#clinical_event"

# Fetch the content of the page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Search for "example" in the document
search_term = "CRITICAL_LOW"


# Initialize a flag to indicate when we find the "FIRST_PROCESS_DT_TM"
found = False
tables = soup.find_all("table")

# Flag to track if "FIRST_PROCESS_DT_TM" is found in any table
found = False

# Loop through each table
for table_index, table in enumerate(tables):
    # Print the table number
    print(f"\nSearching in Table {table_index + 1}:\n")

    # Iterate through the rows of the table
    for row in table.find_all("tr"):
        # Get the columns (td elements) in the row
        columns = row.find_all("td")

        # Check if the row contains three columns
        if len(columns) == 3:
            # Get the value from the first column
            column_value = columns[0].get_text(strip=True)

            # Check if the first column contains "FIRST_PROCESS_DT_TM"
            if column_value == search_term:
                data_type = columns[1].get_text(strip=True)
                description = columns[2].get_text(strip=True)
                print(f"Column Value: {column_value}")
                print(f"Data Type: {data_type}")
                print(f"Description: {description}")
                found = True
                break  # Exit loop once we find the value

    # Stop searching after the first table if we found the value
    if found:
        break

# If "FIRST_PROCESS_DT_TM" was not found in any table
if not found:
    print(f"Value {search_term} not found in any table on the page.")
