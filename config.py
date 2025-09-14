# config.py
# All configuration information

# Names of db and files
DATABASE_NAME = "table_project.db"
DATABASE_FOLDER = "DB"
DATABASE_PATH = f"{DATABASE_FOLDER}/{DATABASE_NAME}"
CONTRACTS_FILE = "projects.txt"
FILE_EXTENSION = ".xlsx"
WORKBOOKS_PATH = "workbooks"

# Table names
TABLE_VARIANCE = "Project Costs"
TABLE_DATA = "start"
TABLE_HOUR = "Hourly and Rate Report"
TABLE_ID_CONTRACT = "ID CONTRACT"

# Excel position contract_id
CONTRACT_NUMBER_ROW = 4
CONTRACT_NUMBER_COL = 2
YEAR_ROW = 5
YEAR_COL = 2

# Settings for the sheet 'Project Costs'
BUDGET_COLUMNS = "C,D,E,F,G"
BUDGET_SKIPROWS = 5
BUDGET_NROWS = 4

# Settings for the sheet 'start'
START_COLUMNS = "B,C"
START_SKIPROWS = 3
START_NROWS = 8
START_DATA_ROWS = [3, 4, 5, 6]  # from iloc

# Settings for the sheet 'Hourly and Rate Report'
HOURS_COLUMNS = "B,C,D,E,F"
HOURS_SKIPROWS = 5
HOURS_NROWS = 20

# Column mapping
COLUMN_MAPPING_VARIANCE = {
    "Group": "group",
    "Cost Breakdown Progress": "cost breakdown progress",
    "Budget": "budget",
    "Cost": "cost",
    "Budget Variance": "budget variance",
}

COLUMN_MAPPING_DATA = {
    "Contract name": "contract name",
    "Project Manage": "project manage",
    "Contract Type": "contract type",
    "Project Start Date": "project start date",
    "Project End Date": "project end date",
    "Country": "country",
}

COLUMN_MAPPING_HOUR = {
    "Week Number": "week number",
    "Working Hours": "working hours",
    "Average Number of People": "average number of people",
    "Work Progress": "work progress",
    "Overtime Hours": "overtime hours",
}

# Encoding
ENCODING = "utf-8"

LOG_LEVEL = "INFO"
