'''
    Script for preparing a dataframe of maintenance work orders for Weibull analysis (adapted from W3-1)
'''

# Ensure that packages are installed
import os
os.system('pip install pandas')

import pandas as pd

from scripts import text_cleaner

def prepare_data(filepath: str, clean_text: bool = True):
    ''' Prepares dataframe for Weibull analysis with optional text cleaning'''

    expected_cols = [
    "id",
    "description",
    "wo_order_type",
    "total_actual_costs",
    "actual_start_date",
    "actual_finish_date",
    "functional_loc_desc",
    "functional_loc",
]

    date_cols = [
        "actual_start_date",
        "actual_finish_date",
    ]

    df = pd.read_csv(
        filepath,
        parse_dates=date_cols,
        dayfirst=True,
        encoding="ISO-8859-1",
        thousands=",",
        dtype={"description": "str", "total_actual_costs": "float"},
    )

    assert set(expected_cols).issubset(
        set(df.columns)
    ), "Uploaded data does not have all the expected columns"

    # Lets remove any records that do not have a short text description
    df = df[~df["description"].isna()]

    # Before we continue we'll convert the functional description into a more unique name for plotting later on
    df["object_desc"] = df["functional_loc_desc"].apply(
        lambda desc: " ".join(
            [word for word in desc.replace("-", " ").split(" ") if word.isalpha()]
        )
    )


    # Clean text and filter on structured data
    df["description"] = df["description"].apply(
        lambda text: text_cleaner.clean_text(text=text)
    )

    # Drop any rows that have no actual_start_date or costs that are nan or less than 0
    df = df[~df["actual_start_date"].isna()]
    df = df[~df["total_actual_costs"].isna()]
    df = df[0 < df["total_actual_costs"]]

    return df