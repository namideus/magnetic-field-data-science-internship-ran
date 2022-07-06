# Summer internship 2022
# Applied Mathematics and Informatics department, AUCA
#
# Created by: Yiman Altynbek uulu

import sys
import numpy as np
from numpy import log
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

# Read file (parsing)
def read_mag_file(fn):
    # Open file
    with open(fn, 'r') as file:
        data_src = file.readlines()

    # Get date indexes in the file
    dates_idx = []
    for idx, row in enumerate(data_src):
        if '/' in row:
            dates_idx.append(idx)

    # add ending label
    dates_idx.append(len(data_src))

    # read daily data chunks
    data = []
    date_stamps = []
    for start_idx, end_idx in zip(dates_idx[:-1], dates_idx[1:]):
        daily_data = data_src[start_idx + 1 : end_idx]
        
        # Get datetime object from UTC
        daily_time = datetime.strptime(data_src[start_idx] + ' 00:00:00', '%Y/%m/%d %H:%M:%S')
        counter = 0

        # Iterate over all the data for a date
        for row in daily_data:
            for elem_str in row.strip().split():
                data.append(float(elem_str))
                # Generate time for each nanotesla
                next_daily_time = daily_time + timedelta(seconds = 20*counter)
                date_stamps.append(next_daily_time)
                counter += 1

    # convert to numpy array
    data = np.array(data)
    data[data==0] = np.nan

    df = pd.DataFrame({'datetime':pd.to_datetime(date_stamps), 'T': data})
    df.set_index('datetime', inplace=True)

    return df

# Read csv file
def read_csv_file(fn):
    # Read csv file
    df = pd.read_csv(fn, names=['datetime', 'T'], skiprows=1)
    # Get datetime from datetime column 
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    return df

# Apply interpolation
def make_interpolation(df, method, order):
    if order:
        # Pandas' interpolation
        df['T_interp'] = df['T'].interpolate(method = method, order = order)
    else:
        df['T_interp'] = df['T'].interpolate(method = method)

    return df

def make_seasonal_decompose(df, start_date, end_date):
    # Original data should stay unchanged
    df_copy = df.copy()
    # Seasonal decompose
    res = seasonal_decompose(df_copy.fillna(value=np.nanmean(df_copy['T'])), period=24*60*3, extrapolate_trend='freq')
    new_df = res.seasonal + res.trend

    # Replace NaNs with "interpolated" values
    for idx, x in enumerate(df_copy['T']):
        if pd.isnull(x):
            df_copy['T'][idx] = new_df[idx] 

    # Seasonal decompose once more for better approximation
    res = seasonal_decompose(df_copy.fillna(value=np.nanmean(df_copy['T'])), period=24*60*3, extrapolate_trend='freq')
    new_df = res.seasonal + res.trend

    df['T_interp'] = df_copy['T']
    df['T_interp'][start_date:end_date] = new_df[start_date:end_date]

    return df

# Test
if __name__ == '__main__':
    df = pd.read_csv('Data/test_original3.csv', names=['datetime', 'T'], skiprows=1)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)


    # new_df.plot(ax=ax[0], color='r', linewidth=2)
    # df['T'].plot(ax=ax[0], color='g', linewidth=2)

    # plt.show()