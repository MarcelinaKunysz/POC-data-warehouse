# import_excel.py
# Main import logic - uses imports from other functions

import sqlite3
from config import *
from database import *
from excel_reader import *
from file_utils import *
from pathlib import Path


def import_excel_to_db(excel_file, db=DATABASE_PATH):
    """Imports data from Excel to database with intelligent update"""

    # Reading all data from Excel - using function from excel_reader.py
    contract_id, df_budget, df_basic, df_hours = read_all_excel_data(excel_file)

    print(f"Processing contract: {contract_id}")

    #Check if db folder exist if not create it - function from database.py
    create_db_folder_if_not_exist()
    
    # Database connection
    conn = sqlite3.connect(db)

    try:
        # Check if database and tables exist - function from database.py
        check_database_ready(conn)
        # Adding contract to ID CONTRACT table - function from database.py
        add_contract_id(conn, contract_id)

        # Checking if contract already exists and updating - functions from database.py
        variance_action = (
            "updated"
            if contract_exists(conn, contract_id, TABLE_VARIANCE)
            else "inserted"
        )
        if variance_action == "updated":
            delete_contract_data(conn, contract_id, TABLE_VARIANCE)

        data_action = (
            "updated" if contract_exists(conn, contract_id, TABLE_DATA) else "inserted"
        )
        if data_action == "updated":
            delete_contract_data(conn, contract_id, TABLE_DATA)

        hour_action = (
            "updated" if contract_exists(conn, contract_id, TABLE_HOUR) else "inserted"
        )
        if hour_action == "updated":
            delete_contract_data(conn, contract_id, TABLE_HOUR)

        # Inserting data into all tables
        df_budget.to_sql(TABLE_VARIANCE, conn, if_exists="append", index=False)
        df_basic.to_sql(TABLE_DATA, conn, if_exists="append", index=False)
        df_hours.to_sql(TABLE_HOUR, conn, if_exists="append", index=False)

        print(
            f"{contract_id}: costs={variance_action}, basic={data_action}, hours={hour_action} ✔"
        )
    except Exception as e:
        print(f"  Error processing contract {contract_id}: {e}")
        conn.rollback()
    finally:
        conn.close()


# Main program logic - uses functions from file_utils.py
if __name__ == "__main__":
    print("Starting import of data from Excel files...")

    # Find all contracts and files - function from file_utils.py
    found, not_found = find_all_contracts_with_files()

    print(f"Found {len(found)} contract files to process")
    print(f"Found {len(not_found)} contract files missing")

    # Counters
    processed = 0

    # Processing each found contract
    for number, file in found:
        p = Path(file)
        print(f"\nProcessing: {p.as_posix()}")
        import_excel_to_db(p.as_posix())
        processed += 1

    # Display not found
    for number in not_found:
        print(f"WARNING: File not found for contract: {number}")

    # Summary
    print(f"\nIMPORT COMPLETED")
    print(f"  - Successfully processed: {processed}")
    print(f"  - Files not found: {len(not_found)}")

    # Display database statistics - function from database.py
    get_database_stats()
