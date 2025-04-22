from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import os
import logging
from contextlib import contextmanager
from ..de.configuration import Configuration
from ..utils.de_utils import *


class DB:
    def __init__(
        self,
        database_type="oracle",
        configuration=None,
    ):
        """
        Creates a connection to either Oracle or SQL Server.

        Parameters:
        - database_type: The type of database. Either 'oracle' or 'sqlserver'.

        Returns:
        - SQLAlchemy engine and session.
        # Define your Oracle and SQL Server connection strings
        # pip install sqlalchemy cx_Oracle pyodbcs
        """
        if configuration == None:
            self.configuration = Configuration()
        else:
            self.configuration = configuration
        ORACLE_CONNECTION_STRING = os.getenv(
            "ORACLE_CONN_STR",
            self.configuration.get("global.ORACLE_CONN_STR"),
        )
        SQLSERVER_CONNECTION_STRING = os.getenv(
            "SQLSERVER_CONN_STR",
            self.configuration.get("global.SQLSERVER_CONN_STR"),
        )  # ;trusted_connection=yes"

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.database_type = database_type
        if database_type == "oracle":
            connection_string = ORACLE_CONNECTION_STRING
        elif database_type == "sqlserver":
            connection_string = SQLSERVER_CONNECTION_STRING
        elif len(database_type) > 1:
            connection_string = SQLSERVER_CONNECTION_STRING.replace(
                "LHI_Dashboard", database_type
            )
        else:
            raise ValueError(
                "Unsupported database type. Choose 'oracle' or 'sqlserver'."
            )
        self.session = None
        self.start_position_chunk = 0
        try:
            # Create engine and session
            engine = create_engine(connection_string, pool_size=10, max_overflow=20)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            # return session, engine
        except SQLAlchemyError as e:
            print(f"Error creating connection: {e}")
            # return None, None

    def extract_data(self, query, params=None):
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
            result = self.session.execute(text(query), params or {}).fetchall()
            df = pd.DataFrame(result)
            return df
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            return None

    def get_next_chunk(self, query, chunk_size=100000):
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
            # Get the connection from the session
            connection = self.session.connection()
            if self.database_type == "oracle":
                paginated_query = f"{query} OFFSET {self.start_position_chunk} ROWS FETCH NEXT {chunk_size} ROWS ONLY"
            else:
                paginated_query = (
                    f"{query} LIMIT {chunk_size} OFFSET {self.start_position_chunk}"
                )
            # print(paginated_query)
            # Now execute the query, with stream_results applied to the connection
            result = connection.execute(
                text(paginated_query), execution_options={"stream_results": True}
            )

            # Loop through the result set in chunks
            rows = result.fetchmany(chunk_size)
            if not rows:
                return False
            self.start_position_chunk = self.start_position_chunk + chunk_size
            return rows
        except SQLAlchemyError as e:
            print(f"Error executing chunk query: {e}")
            return None

    def execute_query_chunk(self, query, chunk_size=100000):
        """
        Execute a raw SQL query using SQLAlchemy session and return the result.

        Parameters:
        - session: The SQLAlchemy session.
        - query: The raw SQL query to execute.

        Returns:
        - Result of the query.
        """
        try:
            chunks = []
            i = 0
            while True:
                processed_chunk = self.get_next_chunk(query, chunk_size)

                if not processed_chunk:
                    break  # No more rows to read, exit the loop
                # Convert chunk to DataFrame (assuming each chunk is a list of rows)
                chunk_df = pd.DataFrame(processed_chunk)
                # Process the chunk (e.g., print or save the rows)
                chunks.append(chunk_df)
                i = i + 1
                # print(i)
            # Loop through the result set in chunks
            df = pd.concat(chunks)

            return df
        except SQLAlchemyError as e:
            print(f"Error executing chunk query: {e}")
            return None

    def extract_data_chunk(self, query, chunk_size=100000):
        """
        Execute a raw SQL query using SQLAlchemy session and return the result.

        Parameters:
        - session: The SQLAlchemy session.
        - query: The raw SQL query to execute.

        Returns:
        - Result of the query.
        """
        try:
            chunks = []
            connection = self.session.connection()
            # print(paginated_query)
            # Now execute the query, with stream_results applied to the connection
            result = connection.execute(
                text(query), execution_options={"stream_results": True}
            )

            # Loop through the result set in chunks
            rows = result.fetchmany(chunk_size)

            i = 0
            while True:
                processed_chunk = result.fetchmany(chunk_size)

                if not processed_chunk:
                    break  # No more rows to read, exit the loop
                # Convert chunk to DataFrame (assuming each chunk is a list of rows)
                chunk_df = pd.DataFrame(processed_chunk)
                # Process the chunk (e.g., print or save the rows)
                chunks.append(chunk_df)
                i = i + 1
                # print(i)
            # Loop through the result set in chunks
            df = pd.concat(chunks)

            return df
        except SQLAlchemyError as e:
            print(f"Error executing chunk query: {e}")
            return None

    def execute_query(self, query):
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
            result = self.session.execute(text(query)).fetchall()
            return result
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            return None

    def close_connection(self):
        """Close the session and connection."""
        try:
            self.session.close()
        except SQLAlchemyError as e:
            print(f"Error closing session: {e}")

    def save_DF(self, df, file_name, file_folder=None):
        if file_folder is None:

            return save_toDF(
                df,
                file_name + ".csv",
                os.path.join(
                    self.configuration.get("global.project.path"),
                    self.configuration.get("global.db_path"),
                ),
            )
        else:
            return save_toDF(df, file_name, file_folder)

    def read_DF(self, file_name):
        return read_toDF(
            file_name + ".csv",
            os.path.join(
                self.configuration.get("global.project.path"),
                self.configuration.get("global.db_path"),
            ),
        )

    def read_DF_file_existing(self, file_name):
        file_path = os.path.join(
            self.configuration.get("global.project.path"),
            self.configuration.get("global.db_path"),
            file_name + ".csv",
        )
        if os.path.exists(file_path):
            return True
        else:
            return False

    # Function to generate a data dictionary for the entire database
    def data_dictionary(self, table_name_range=None, filename="data_dictionary.csv"):

        # Get all tables in the database

        tables = self.session.execute(
            text(
                """
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            
            """
                # WHERE TABLE_TYPE = 'BASE TABLE'
            )
        ).fetchall()
        data_dict = {}
        for table in tables:
            table_name = table[0]
            if table_name_range != None:
                table_name_range = "^" + table_name_range + "$"
                if not regex_match(table_name_range, table_name, True):
                    continue
            # Get all columns for each table
            columns = self.session.execute(
                text(
                    f"""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """
                )
            ).fetchall()

            # Store table information in the dictionary
            columns_info = []
            for column in columns:
                column_info = {
                    "column_name": column[0],
                    "data_type": column[1],
                    "max_length": column[2],
                    "numeric_precision": column[3],
                    "numeric_scale": column[4],
                }
                columns_info.append(column_info)

            data_dict[table_name] = columns_info

        rows = []

        for table_name, columns in data_dict.items():
            for column in columns:
                row = {
                    "table_name": table_name,
                    "column_name": column["column_name"],
                    "data_type": column["data_type"],
                    "max_length": column["max_length"],
                    "numeric_precision": column["numeric_precision"],
                    "numeric_scale": column["numeric_scale"],
                }
                rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        return df

    def cerner_dictionary(self, table_name_range=None, filename="data_dictionary.csv"):

        # Get all tables in the database

        tables = self.session.execute(
            text(
                """
                SELECT TABLE_NAME
                FROM user_tables
                order by 1
                """
                # WHERE TABLE_TYPE = 'BASE TABLE'
            )
        ).fetchall()
        data_dict = {}
        for table in tables:
            table_name = table[0]
            if table_name_range != None:
                table_name_range = "^" + table_name_range + "$"
                if not regex_match(table_name_range, table_name, True):
                    continue
            # Get all columns for each table
            columns = self.session.execute(
                text(
                    # Query to retrieve column details for the table
                    f"""
                    SELECT 
                        column_name, 
                        data_type, 
                        data_length as max_length, 
                        data_precision as numeric_precision, 
                        data_scale as numeric_scale, 
                        nullable, 
                        column_id 
                    FROM 
                        all_tab_columns
                    WHERE 
                        table_name = '{table_name.upper()}'
                    ORDER BY 
                        column_id
                    """
                )
            ).fetchall()

            # Store table information in the dictionary
            columns_info = []
            for column in columns:
                column_info = {
                    "column_name": column[0],
                    "data_type": column[1],
                    "max_length": column[2],
                    "numeric_precision": column[3],
                    "numeric_scale": column[4],
                    "nullable": column[5],
                    "column_id": column[6],
                }
                columns_info.append(column_info)

            data_dict[table_name] = columns_info

        rows = []

        for table_name, columns in data_dict.items():
            for column in columns:
                row = {
                    "table_name": table_name,
                    "column_name": column["column_name"],
                    "data_type": column["data_type"],
                    "max_length": column["max_length"],
                    "numeric_precision": column["numeric_precision"],
                    "numeric_scale": column["numeric_scale"],
                    "nullable": column["nullable"],
                    "column_id": column["column_id"],
                }

                rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        return df
