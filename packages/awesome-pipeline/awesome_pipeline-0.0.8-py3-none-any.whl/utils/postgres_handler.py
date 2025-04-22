import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor


class PostgresHandler:
    def __init__(self, db_name=None, user=None, password=None, host=None, port=None):
        """
        Initialize the PostgreSQL database connection using environment variables.
        - db_name: The database name, can be provided or fetched from the 'DB_NAME' environment variable.
        - user: The username for the database, can be provided or fetched from 'DB_USER' environment variable.
        - password: The password for the database, can be provided or fetched from 'DB_PASSWORD' environment variable.
        - host: Database host, defaults to 'localhost'.
        - port: Database port, defaults to '5432'.
        """
        self.db_name = db_name or os.getenv("DB_NAME", "postgres")
        self.user = user or os.getenv("POSTGRES_USER", "postgres")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "postgres")
        self.host = host or os.getenv("DB_HOST", "127.0.0.1")
        self.port = port or os.getenv("DB_PORT", "5432")
        self.conn = None

    def connect(self):
        """Establish connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None, fetch=False, fetchall=True):
        """
        Execute a custom SQL query. Optionally fetch results.
        - `params`: Optional parameters for a parameterized query.
        - `fetch`: Set to True if the query returns data (e.g., SELECT).
        - `fetchall`: Set to True to fetch all rows, otherwise fetch only one.
        """
        result = None
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                result = cur.fetchall() if fetchall else cur.fetchone()
            self.conn.commit()
        return result

    def create_table_if_not_exists(self, table_name, column_definitions):
        with self.conn.cursor() as cur:
            create_table_query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {table} (
                    {columns}
                );
            """
            ).format(
                table=sql.Identifier(table_name), columns=sql.SQL(column_definitions)
            )
            cur.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created or already exists.")

    def insert(self, table, data):
        """Insert a record into a specific table. We use autoincrease id to uniquely identify each record"""
        with self.conn.cursor() as cur:
            columns = data.keys()
            values = data.values()
            insert_query = sql.SQL(
                "INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
            ).format(
                table=sql.Identifier(table),
                columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
                values=sql.SQL(", ").join(sql.Placeholder() * len(values)),
            )
            cur.execute(insert_query, tuple(values))
            self.conn.commit()
            inserted_id = cur.fetchone()[0]  # Return the id of the inserted record
            print(f"Inserted record with ID: {inserted_id}")
            return inserted_id

    def update(self, table, data, where_clause):
        """Update rows in a specific table based on a condition."""
        with self.conn.cursor() as cur:
            set_clause = ", ".join(f"{col} = %s" for col in data.keys())
            where_clause_str = " AND ".join(
                f"{col} = %s" for col in where_clause.keys()
            )
            update_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause_str}"

            cur.execute(
                update_query, tuple(data.values()) + tuple(where_clause.values())
            )
            self.conn.commit()
            print(f"Updated rows in table: {table}")

    def delete(self, table, where_clause):
        """Delete rows from a specific table based on a condition."""
        with self.conn.cursor() as cur:
            where_clause_str = " AND ".join(
                f"{col} = %s" for col in where_clause.keys()
            )
            delete_query = f"DELETE FROM {table} WHERE {where_clause_str}"

            cur.execute(delete_query, tuple(where_clause.values()))
            self.conn.commit()
            print(f"Deleted rows from table: {table}")

    def add_column(self, table, column_name, column_type):
        """Add a new column to a table."""
        with self.conn.cursor() as cur:
            alter_query = sql.SQL(
                "ALTER TABLE {table} ADD COLUMN {column_name} {column_type}"
            ).format(
                table=sql.Identifier(table),
                column_name=sql.Identifier(column_name),
                column_type=sql.SQL(column_type),
            )
            cur.execute(alter_query)
            self.conn.commit()
            print(f"Added column {column_name} to table {table}.")

    def fetch_records(self, table, columns="*", where_clause=None, limit=None):
        """
        Fetch records from a table.
        - `columns`: List of columns to fetch, or `*` for all.
        - `where_clause`: Optional dictionary for filtering rows.
        - `limit`: Optional integer to limit the number of rows fetched.
        """
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = sql.SQL("SELECT {columns} FROM {table}").format(
                columns=(
                    sql.SQL(", ").join(map(sql.Identifier, columns))
                    if isinstance(columns, list)
                    else sql.SQL(columns)
                ),
                table=sql.Identifier(table),
            )

            if where_clause:
                where_clause_str = " AND ".join(
                    f"{col} = %s" for col in where_clause.keys()
                )
                query = query + sql.SQL(f" WHERE {where_clause_str}")

            if limit:
                query = query + sql.SQL(f" LIMIT {limit}")

            cur.execute(query, tuple(where_clause.values()) if where_clause else None)
            result = cur.fetchall()
            return result
