# excel_reader.py

import pandas as pd
from config import *


def extract_contract_id(excel_file):
    """Extracts contract ID from 'start' sheet"""
    start_sheet = pd.read_excel(excel_file, sheet_name="start", header=None)
    contract_numer = start_sheet.iloc[CONTRACT_NUMBER_ROW, CONTRACT_NUMBER_COL]
    year = start_sheet.iloc[YEAR_ROW, YEAR_COL]
    contract_id = f"{contract_numer}_{year}"
    return contract_id


def read_budget_data(excel_file, contract_id):
    """Reads budget data from 'Project Costs' sheet"""
    df = pd.read_excel(
        excel_file,
        sheet_name="Project Costs",
        usecols=BUDGET_COLUMNS,
        skiprows=BUDGET_SKIPROWS,
        nrows=BUDGET_NROWS,
        header=0,
    )

    # Change column names
    df = df.rename(columns=COLUMN_MAPPING_VARIANCE)
    df["contract_id"] = contract_id
    return df


def read_basic_data(excel_file, contract_id):
    """Reads basic contract data from 'start' sheet"""
    df_basic = pd.read_excel(
        excel_file,
        sheet_name="start",
        usecols=START_COLUMNS,
        skiprows=START_SKIPROWS,
        nrows=START_NROWS,
    )
    df_basic = df_basic.iloc[START_DATA_ROWS]
    df_basic = df_basic.T
    df_basic.columns = df_basic.iloc[0]
    df_basic = df_basic.drop(df_basic.index[0])
    df_basic.reset_index(drop=True, inplace=True)

    # Change column names
    df_basic = df_basic.rename(columns=COLUMN_MAPPING_DATA)
    df_basic["contract_id"] = contract_id
    return df_basic


def read_hours_data(excel_file, contract_id):
    """Reads hours data from 'Hourly and Rate Report' sheet"""
    df_hours = pd.read_excel(
        excel_file,
        sheet_name="Hourly and Rate Report",
        usecols=HOURS_COLUMNS,
        skiprows=HOURS_SKIPROWS,
        nrows=HOURS_NROWS,
    )
    df_hours = df_hours.dropna(how="all")
    df_hours = df_hours[df_hours["Week Number"] != "Sum"]

    # Change column names
    df_hours = df_hours.rename(columns=COLUMN_MAPPING_HOUR)
    df_hours["contract_id"] = contract_id
    return df_hours


def read_all_excel_data(excel_file):
    """Reads all data from Excel file - main function"""
    contract_id = extract_contract_id(excel_file)

    df_budget = read_budget_data(excel_file, contract_id)
    df_basic = read_basic_data(excel_file, contract_id)
    df_hours = read_hours_data(excel_file, contract_id)

    return contract_id, df_budget, df_basic, df_hours
