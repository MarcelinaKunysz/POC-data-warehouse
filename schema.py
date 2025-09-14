# schema.py
# Database schema definitions - table structures only

from config import *


def create_tables_if_not_exist(conn):
    """Creates tables if they don't exist - ONLY table definitions here"""
    cursor = conn.cursor()

    # Table for budget deviation
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{TABLE_VARIANCE}" (
            contract_id TEXT,
            "group" TEXT,
            "cost breakdown progress" INTEGER,
            "budget" REAL,
            "cost" REAL,
            "budget variance" REAL,
            PRIMARY KEY (contract_id, "group")
        )
    """
    )

    # Table for basic contract data
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{TABLE_DATA}" (
            contract_id TEXT PRIMARY KEY,
            "contract name" TEXT,
            "project manage" TEXT,
            "contract type" TEXT,
            "project start date" DATE,
            "project end date" DATE,
            "country" TEXT
        )
    """
    )

    # Table for hours and rates report
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{TABLE_HOUR}" (
            contract_id TEXT,
            "week number" INTEGER,
            "working hours" INTEGER,
            "average number of people" INTEGER,
            "work progress" REAL,
            "overtime hours" TEXT,
            PRIMARY KEY (contract_id, "week number")
        )
    """
    )

    # Table ID CONTRACT
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{TABLE_ID_CONTRACT}" (
            contract_id TEXT PRIMARY KEY
        )
    """
    )

    conn.commit()


def drop_all_tables(conn):
    """Drops all tables - useful for complete reset"""
    cursor = conn.cursor()

    tables = [TABLE_VARIANCE, TABLE_DATA, TABLE_HOUR, TABLE_ID_CONTRACT]
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS "{table}"')

    conn.commit()
    print("All tables dropped")
