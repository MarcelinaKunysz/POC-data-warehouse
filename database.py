# database.py
# Functions for database management - CRUD operations only

import sqlite3
from config import *
from schema import create_tables_if_not_exist


def add_contract_id(conn, contract_id):
    """Adds contract to ID CONTRACT table if it doesn't exist"""
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT OR IGNORE INTO "{TABLE_ID_CONTRACT}" (contract_id) VALUES (?)',
        (contract_id,),
    )
    conn.commit()


def contract_exists(conn, contract_id, table_name):
    """Checks if contract already exists in table"""
    return (
        conn.cursor()
        .execute(
            f'SELECT COUNT(*) FROM "{table_name}" WHERE contract_id = ?',
            (contract_id,),
        )
        .fetchone()[0]
        > 0
    )


def delete_contract_data(conn, contract_id, table_name):
    """Deletes contract data from table"""
    cursor = conn.cursor()
    cursor.execute(
        f'DELETE FROM "{table_name}" WHERE contract_id = ?',
        (contract_id,),
    )
    conn.commit()


def check_database_ready(conn):
    """Check if database has required tables; create them if missing"""
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{TABLE_ID_CONTRACT}" LIMIT 1')
        return True
    except sqlite3.OperationalError:
        print("Database not ready – creating tables...")
        create_tables_if_not_exist(conn)
        return True


def get_database_stats(db=DATABASE_PATH):
    """Display database statistics"""
    try:
        conn = sqlite3.connect(db)

        check_database_ready(conn)

        cursor = conn.cursor()

        # Number of contracts in variance table
        cursor.execute(f'SELECT COUNT(DISTINCT contract_id) FROM "{TABLE_VARIANCE}"')
        variance_count = cursor.fetchone()[0]

        # Number of contracts in basic data table
        cursor.execute(f'SELECT COUNT(*) FROM "{TABLE_DATA}"')
        data_count = cursor.fetchone()[0]

        # Number of contracts in hours table
        cursor.execute(f'SELECT COUNT(DISTINCT contract_id) FROM "{TABLE_HOUR}"')
        hour_count = cursor.fetchone()[0]

        print(f"\nDatabase statistics:")
        print(f"  - Contracts with deviation data: {variance_count}")
        print(f"  - Contracts with basic data: {data_count}")
        print(f"  - Contracts with hours data: {hour_count}")

        conn.close()
    except Exception as e:
        print(f"Cannot read statistics: {e}")
