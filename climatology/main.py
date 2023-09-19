# climate row is from jan 1892 to aug 2023

import pandas as pd
import numpy as np

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
    dikson_row = cur_df.sort_values(by=month)

    # statistic
    avg = dikson_row[month].sum() / n
    max_value = dikson_row[month].max()
    min_value = dikson_row[month].min()
    std_temp = dikson_row[month].std()
    nulls_count = cur_df[month].isnull().sum().sum()

    try:
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

        mark_max = None

    except:
        d1_max, d2_max, d3_max, d4_max, d5_max = None, None, None, None, None
        if nulls_count > 0:
            mark_max = "ряд неполон"
        else:
            mark_max = "в ряду несколько максимумов"

    try:
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

        mark_min = None

    except:
        d1_min, d2_min, d3_min, d4_min, d5_min = None, None, None, None, None
        if nulls_count > 0:
            mark_min = "ряд неполон"
        else:
            mark_min = "в ряду несколько максимумов"

    # Smirnov-Grabbs criteria
    if nulls_count == 0:
        sg_max = round((dikson_row.at[n - 1, month] - avg) / std_temp, 2)
        sg_min = round((avg - dikson_row.at[0, month]) / std_temp, 2)
        mark_sg = None
    else:
        sg_max = round((dikson_row.at[n - 1 - nulls_count, month] - avg) / std_temp, 2)
        sg_min = round((avg - dikson_row.at[0, month]) / std_temp, 2)
        mark_sg = "Сомнительное значение, в ряду встречаются пропуски"

    statistic_dict[month] = {"Nulls_count": nulls_count, "Max": max_value, "Min": min_value,
                             "Average": round(avg, 1), "STD": round(std_temp, 1),
                             "Dixon": {"TO_MAX": {"D1": d1_max, "D2": d2_max, "D3": d3_max,
                                                  "D4": d4_max, "D5": d5_max,
                                                  "mark_max": mark_max},
                                       "TO_MIN": {"D1": d1_min, "D2": d2_min,
                                                  "D3": d3_min, "D4": d4_min, "D5": d5_min,
                                                  "mark_min": mark_min}},
                             "Smirnov-Grabbs": {"SG_MAX": sg_max, "SG_MIN": sg_min, "mark_sg": mark_sg}}
# print(values)
print(statistic_dict)
