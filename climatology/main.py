# climate row is from jan 1892 to aug 2023
# 12 months and annual values
import os

# pip install openpyxl
# pip install XlsxWriter

import pandas as pd
import numpy as np
from pandas import ExcelWriter

# years row creating -> dataframe
years_list = list(range(1892, 2023 + 1))
years = pd.DataFrame(years_list, columns=['year'])

# data loading and all data df creating
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'all_year_val']
values = pd.read_csv('saloniky_climate_rows.txt', skiprows=1, delimiter="\t", names=months)
values.insert(0, 'year', years['year'])
values = values.replace([999.9], None)
print(values)

n = len(years_list)
statistic_dict = {}

for month in months:
    cur_df = values[['year', month]]

    # statistic
    avg = cur_df[month].sum() / n
    max_value = cur_df[month].max()
    min_value = cur_df[month].min()
    std_temp = cur_df[month].std()
    nulls_count = cur_df[month].isnull().sum().sum()
    nulls_percentage = nulls_count / n * 100

    # None values recovery
    if nulls_percentage <= 10:

        cur_df = cur_df.fillna(avg)
        dikson_row = cur_df.sort_values(by=month)
        print(dikson_row.head())
        print(dikson_row.tail())
        # dikson criteria
        d1_max = round((dikson_row.at[n - 1, month] - dikson_row.at[n - 2, month]) / (
                dikson_row.at[n - 1, month] - dikson_row.at[0, month]), 2)
        d2_max = round((dikson_row.at[n - 1, month] - dikson_row.at[n - 2, month]) / (
                dikson_row.at[n - 1, month] - dikson_row.at[1, month]), 2)
        d3_max = round((dikson_row.at[n - 1, month] - dikson_row.at[n - 3, month]) / (
                dikson_row.at[n - 1, month] - dikson_row.at[1, month]), 2)
        d4_max = round((dikson_row.at[n - 1, month] - dikson_row.at[n - 3, month]) / (
                dikson_row.at[n - 1, month] - dikson_row.at[2, month]), 2)
        d5_max = round((dikson_row.at[n - 1, month] - dikson_row.at[n - 3, month]) / (
                dikson_row.at[n - 1, month] - dikson_row.at[0, month]), 2)

        d1_min = round((dikson_row.at[0, month] - dikson_row.at[1, month]) / (
                dikson_row.at[0, month] - dikson_row.at[n - 1, month]), 2)
        d2_min = round((dikson_row.at[0, month] - dikson_row.at[1, month]) / (
                dikson_row.at[0, month] - dikson_row.at[n - 2, month]), 2)
        d3_min = round((dikson_row.at[0, month] - dikson_row.at[2, month]) / (
                dikson_row.at[0, month] - dikson_row.at[n - 2, month]), 2)
        d4_min = round((dikson_row.at[0, month] - dikson_row.at[2, month]) / (
                dikson_row.at[0, month] - dikson_row.at[n - 3, month]), 2)
        d5_min = round((dikson_row.at[0, month] - dikson_row.at[2, month]) / (
                dikson_row.at[0, month] - dikson_row.at[n - 1, month]), 2)

        # Smirnov-Grabbs criteria
        sg_max = round((dikson_row.at[n - 1, month] - avg) / std_temp, 2)
        sg_min = round((avg - dikson_row.at[0, month]) / std_temp, 2)

        if nulls_count > 0:
            mark = (f"Количество пропусков в ряду {round(nulls_percentage, 2)}%, "
                    f"произведена замена значений None на среднее ряда")
        else:
            mark = None

        statistic_df = pd.DataFrame([["Nulls_count", nulls_count, None, None],
                                     ["Max", max_value, None, None],
                                     ["Min", min_value, None, None],
                                     ["Average", round(avg, 1), None, None],
                                     ["STD", round(std_temp, 1), None, None],
                                     ["Dixon", None, None, None],
                                     ["TO MAX", None, "TO MIN", None],
                                     ["D1", d1_max, "D1", d1_min],
                                     ["D2", d2_max, "D2", d2_min],
                                     ["D3", d3_max, "D3", d3_min],
                                     ["D4", d4_max, "D4", d4_min],
                                     ["D5", d5_max, "D5", d5_min],
                                     ["Smirnov-Grabbs", None, None, None],
                                     ["SG_MAX", sg_max, "SG_MIN", sg_min],
                                     ["Mark", mark, None, None]])

        with pd.ExcelWriter('statistic_params.xlsx', engine="openpyxl",
                            mode="a" if os.path.exists('statistic_params.xlsx') else "w") as writer:
            statistic_df.to_excel(writer, sheet_name=month)

    else:
        print(f"Большое количество пропусков: {round(nulls_percentage, 2)}% в ряду {month}, восстановите значения, либо"
              f" измените порог nulls_percentage")

