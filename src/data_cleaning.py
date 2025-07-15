import re

import pandas as pd
from dateparser import parse


def extract_language(text):
    if pd.isnull(text):
        return "English"
    match = re.search(r'See original \((.*?)\)', text)
    if match:
        return match.group(1)
    return None

def clean_date(date_series, reference_date="2025-07-10"):
    if isinstance(reference_date, str):
        reference_date = pd.to_datetime(reference_date)

    def parse_date(x):
        x = x.replace("Edited ", "")
        return parse(x, settings={"RELATIVE_BASE": reference_date}) if x else None

    parsed_dates = date_series.apply(parse_date)
    parsed_period = parsed_dates.dt.year
    return parsed_period

def keep_relevant_columns(df):
    df_clean = df.loc[:, ["d4r55", "rsqaWe", "kyuRq", "wiI7pd"]].copy()
    df_clean.columns = ["reviewer", "year", "original_language", "content"]
    return df_clean