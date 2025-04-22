import pyodbc

# List all available ODBC drivers on your system
drivers = [driver for driver in pyodbc.drivers()]
print(drivers)
