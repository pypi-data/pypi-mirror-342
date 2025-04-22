from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import os
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Define your Oracle and SQL Server connection strings
# pip install sqlalchemy cx_Oracle pyodbcs
ORACLE_CONNECTION_STRING = os.getenv(
    "ORACLE_CONN_STR", "oracle+cx_oracle://v500:v500@svdcemr-sdb016.nswhealth.net:1521/?service_name=kidsp.world",
)

SQLSERVER_CONNECTION_STRING = os.getenv(
    "SQLSERVER_CONN_STR",
    "mssql+pyodbc://sa:Password99@MSAURPT01/LHI_Dashboard?driver=ODBC+Driver+17+for+SQL+Server",
)  # ;trusted_connection=yes"

import logging

logging.basicConfig(level=logging.INFO)


def create_connection(database_type="oracle"):
    """
    Creates a connection to either Oracle or SQL Server.

    Parameters:
    - database_type: The type of database. Either 'oracle' or 'sqlserver'.

    Returns:
    - SQLAlchemy engine and session.
    """
    if database_type == "oracle":
        connection_string = ORACLE_CONNECTION_STRING
    elif database_type == "sqlserver":
        connection_string = SQLSERVER_CONNECTION_STRING
    else:
        raise ValueError("Unsupported database type. Choose 'oracle' or 'sqlserver'.")

    try:
        # Create engine and session
        engine = create_engine(connection_string, pool_size=10, max_overflow=20)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session, engine
    except SQLAlchemyError as e:
        print(f"Error creating connection: {e}")
        return None, None


def extract_data(session, query, params=None):
    """
    Extract data from the database using SQLAlchemy.

    Parameters:
    - session: The SQLAlchemy session.
    - query: The SQL query to execute.
    - params: Optional dictionary for query parameters.

    Returns:
    - A pandas DataFrame containing the query results.
    """
    try:
        # Execute the query and fetch the result into a pandas DataFrame
        result = session.execute(text(query), params or {}).fetchall()
        df = pd.DataFrame(result)
        return df
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None


def execute_query(session, query):
    """
    Execute a raw SQL query using SQLAlchemy session and return the result.

    Parameters:
    - session: The SQLAlchemy session.
    - query: The raw SQL query to execute.

    Returns:
    - Result of the query.
    """
    try:
        # Wrap query in SQLAlchemy text() to handle raw SQL properly
        result = session.execute(text(query)).fetchall()
        return result
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None


def close_connection(session):
    """Close the session and connection."""
    try:
        session.close()
    except SQLAlchemyError as e:
        print(f"Error closing session: {e}")

def save_toDF(df,file_name):
    df.to_csv(os.path.join("C:\Users\60265683\git\data_pipeline\data",file_name),index=False)
def read_toDF(file_name):
    return pd.read_csv(os.path.join("C:\Users\60265683\git\data_pipeline\data", file_name))

# Example usage
if __name__ == "__main__":
    # Create connection for Oracle or SQL Server
    database_type = "oracle"  # Choose "oracle" or "sqlserver"
    # database_type = "oracle"  # Choose "oracle" or "sqlserver"
    session, engine = create_connection(database_type)

    if session:
        if database_type == "sqlserver":
            query = "SELECT * FROM Encounter WHERE encounter_id = 69604454"
        else:
            query = "SELECT code_value, description FROM code_value"
        print(f"Connected to {database_type} Server!")

        result = extract_data(session, query)
        save_toDF(result,"code_value")
        print(result)

        # if result:
        #     print("Query executed successfully!")
        #     for row in result:
        #         print(row)  # Print the result rows

        # Close the session after work is done
        close_connection(session)
