from pydsstools.heclib.dss import HecDss
import pandas as pd
from datetime import timedelta
import numpy as np
from pydsstools.heclib.utils import dss_logging

# turn off all the dss output
dss_logging.config(level='None')


def read_evap_data(s_path, s_b_part):
    """
    Reads in the evap rates from the evap DSS file
    Parameters
    ----------
    s_path: str
        Path to DSS file
    s_b_part:str
        B part for reading from the DSS file

    Returns
    -------
    df_dss_data: dataframe
        Data from the DSS file corresponding to the B part
    """

    # open the DSS file
    o_file = HecDss.Open(s_path)

    # get the potential paths for this b part
    ls_paths = o_file.search_path(f"/CALSIM/{s_b_part}/EVAPORATION-RATE/*/*/*/")

    # if there are no paths, it doesn't exist and we want to fail
    if ls_paths == []:
        raise Exception(f"No paths found for {s_b_part} in {s_path}")

    # get the path but replace the date with a blank so we get the full timeseries
    ls_final_path = ls_paths[0].split('/')
    ls_final_path[4] = ''
    s_final_path = '/'.join(ls_final_path)

    # read the timeseries in
    o_timeseries = o_file.read_ts(s_final_path, trim_missing=True)

    # check that it is not empty
    if o_timeseries.empty:
        raise Exception(f"Empty timeseries at path: {s_final_path}")

    # put it in a dataframe with the units as the column name
    ol_times = [o_time.datetime() for o_time in o_timeseries.times]
    df_dss_data = pd.DataFrame(o_timeseries.values, index=ol_times, columns=[o_timeseries.data_units])

    # adjust the dates to match what they should be
    df_dss_data.index = df_dss_data.index + timedelta(days=-1)

    # return the dataframe
    return df_dss_data.copy()


def calculate_evap_data(df_storage_data, df_evap_rates, df_area_capacity, b_set_zeros=True):
    """
    Calculate the evaporation amounts based on the rates and storage
    Parameters
    ----------
    df_storage_data: dataframe
        Storage data for the reservoir
    df_evap_rates: dataframe
        Evaporation rates for the reservoir
    df_area_capacity: dataframe
        Area capacity relationship for the reservoir
    d_max_cap: float
        Max capacity for the reservoir (TAF)
    d_max_area: float
        Max area for the reservoir (Acres)
    b_set_zeros: bool
        Flag for if

    Returns
    -------
    df_evaporation_data: dataframe
        Evaporation data for the reservoir
    """

    # if the storage data is a series, convert to dataframe
    if isinstance(df_storage_data, pd.Series):
        df_storage_data = pd.DataFrame(df_storage_data)
        df_storage_data.columns = ['TAF']

    # get the storage averages
    df_storage_data['Averages'] = (df_storage_data['TAF'] + df_storage_data['TAF'].shift(1)) / 2

    # evap rates are in inches, convert to feet
    df_evap_rates['Feet'] = df_evap_rates['IN']/12

    # create empty evap dataframe that we will fill
    df_evaporation_data = pd.DataFrame(index=df_evap_rates.index, columns=['TAF'], dtype='float')

    # loop through the storage timeseries
    for index, row in df_storage_data.iterrows():
        # check if the row is nans
        if row.isna().any():
            df_evaporation_data.loc[index, 'TAF'] = np.nan

        elif b_set_zeros and row.iloc[0] == 0:
            df_evaporation_data.loc[index, 'TAF'] = 0

        else:
            # linearly interpolate the capacities to get the area
            # value for the current capacity. units are acres here

            # TODO: from numpy This returns fp[-1] for x > xp[-1],
            # which means it does not extrapolate outside range, but
            # exce FORECAST function does, we might have to change it
            # to make it the same
            d_pred_area = np.interp(row['Averages'], df_area_capacity['Capacity'], df_area_capacity['Area'])

            # multiply by the evap rate
            df_evaporation_data.loc[index, 'TAF'] = d_pred_area * df_evap_rates.loc[index, 'Feet'] / 1000

    # return the dataframe
    return df_evaporation_data.copy()


def calc_evap_11427400(s_dss_file, df_storage_data):
    """
    Calculates the evaporation amount for USGS 11427400 FRENCH MEADOWS RES NR FORESTHILL CA; CDEC ID FMD FRENCH MEADOWS. Follows the logic in CS3_I_FRMDW_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FRMDW')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11427400_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11427400_evap'] = calculate_evap_data(df_storage_data['11427400'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_11436950(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11436950 CAPLES LK NR KIRKWOOD CA; CDEC CAPLES LAKE (PG&E) (CPL). Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_CAPLS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11436950_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [23, 620]

    # update the one area that needs to be raised. this is done in the sheet
    df_area_capacity.loc[10, 'Area'] = 596

    # calculate and set the evaporation
    df_storage_data['11436950_evap'] = calculate_evap_data(df_storage_data['11436950'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)


def calc_evap_11435900(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11435900 SILVER LK NR KIRKWOOD CA; CDEC SILVER LAKE RESERVOIR (SIV). Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SILVR')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11435900_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [8.792, 385]

    # calculate and set the evaporation
    df_storage_data['11435900_evap'] = calculate_evap_data(df_storage_data['11435900'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)


def calc_evap_11434900(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11434900 LK ALOHA NR PHILLIPS(MEDLEY LAKE) CA. Follows the logic in CS3_I_SFA006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # the original need uses different evap rates from the dss file so we will pull from a csv
    df_evap_rates = read_evap_data(s_dss_file, 'ER_ALOHA')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11434900_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (AF)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (AF)'].shift(1) - df_area_capacity['Capacity (AF)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # add in a row with a maximum capacity and area
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [5.35, 627]

    # adjust one elevation to match the sheet
    df_area_capacity.loc[7, 'Capacity'] = df_area_capacity.loc[6, 'TAF']

    # set teh first row to be slighltly above 0 to match the sheet
    df_area_capacity.loc[0, ['Capacity', 'Area']] = [0.001, 0.001]

    # calculate and set the evaporation
    df_storage_data['11434900_evap'] = calculate_evap_data(df_storage_data['11434900'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11428700(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11428700 HELL HOLE RES NR MEEKS BAY CA. Follows the logic in CS3_I_HHOLE_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_HHOLE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11428700_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (AF)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (AF)'].shift(1) - df_area_capacity['Capacity (AF)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11428700_evap'] = calculate_evap_data(df_storage_data['11428700'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11429350(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11429350 LOON LK NR MEEKS BAY CA. Follows the logic in CS3_I_LOONL_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LOONL')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11429350_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 1450
    df_area_capacity.loc[df_area_capacity['Area'] > 1450, 'Area'] = 1450

    # calculate and set the evaporation
    df_storage_data['11429350_evap'] = calculate_evap_data(df_storage_data['11429350'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11429600(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11429600 GERLE RES NR MEEKS BAY CA. Follows the logic in CS3_I_SFR006_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_GERLE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11429600_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # uses straight data not averages
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['TAF']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 50
    df_area_capacity.loc[df_area_capacity['Area'] > 50, 'Area'] = 50

    # calculate and set the evaporation
    df_storage_data['11429600_evap'] = calculate_evap_data(df_storage_data['11429600'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_EDN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC EDN STUMPY MEADOWS RESERVOIR (MARK EDSON DAM). Follows the logic in CS3_I_STMPY_Rev2022G

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_STMPY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/EDN_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # make sure none of the areas are above a maximum of 330
    df_area_capacity.loc[df_area_capacity['Area'] > 330, 'Area'] = 330

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [20.0001, 330]

    # calculate and set the evaporation
    df_storage_data['EDN_evap'] = calculate_evap_data(df_storage_data['EDN'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11426170(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11426170 LAKE VALLEY RESERVOIR NEAR CISCO  CA. Follows the logic in CS3_I_LKVLY_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LKVLY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11426170_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 312
    df_area_capacity.loc[df_area_capacity['Area'] > 312, 'Area'] = 312

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [8.4, 312]

    # calculate and set the evaporation
    df_storage_data['11426170_evap'] = calculate_evap_data(df_storage_data['11426170'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11441000(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11441001 UNION VALLEY RES NR RIVERTON CA. Follows the logic in CS3_I_UNVLY_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_UNVLY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11441001_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)


    # calculate and set the evaporation
    df_storage_data['11441001_evap'] = calculate_evap_data(df_storage_data['11441001'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11441100(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11441100 ICE HOUSE RES NR KYBURZ CA. Follows the logic in CS3_I_UNVLY_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_ICEHS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11441100_AC.csv")

    # no calculations, just rename columns
    df_area_capacity.rename(columns={'Storage (TAF)': 'Capacity', 'Area (acres)': 'Area'}, inplace=True)

    # calculate and set the evaporation
    df_storage_data['11441100_evap'] = calculate_evap_data(df_storage_data['11441100'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)


def calc_evap_folsom(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Folsom Reservoir. Follows the logic in CS3_I_FOLSM_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FOLSM')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/folsom_AC.csv")

    # no calculations, just rename columns
    df_area_capacity.rename(columns={'Capacity (TAF)': 'Capacity', 'Area (acres)': 'Area'}, inplace=True)

    # calculate and set the evaporation
    df_storage_data['Folsom_evap_calculated'] = calculate_evap_data(df_storage_data['Folsom'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)


def calc_evap_NAT(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Lake Natoma. Follows the logic in CS3_I_FOLSM_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_NTOMA')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/NAT_AC.csv")

    # Rename column
    df_area_capacity.rename(columns={'Area (acres)': 'Area'}, inplace=True)

    # get capacity in TAF
    df_area_capacity['Capacity'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # calculate and set the evaporation
    df_storage_data['NAT_evap_calculated'] = calculate_evap_data(df_storage_data['NAT'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], False)

def calc_evap_NHGAN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for New Hogan Reservoir. Follows the logic in CS3_I_NHGAN_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_NHGAN')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/NHGAN_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 4410
    df_area_capacity.loc[df_area_capacity['Area'] > 4410, 'Area'] = 4410

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [317.123, 4410]

    # calculate and set the evaporation
    df_storage_data['NHGAN_evap'] = calculate_evap_data(df_storage_data['NHGAN_STORAGE'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_OHGAN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Old Hogan Reservoir. Follows the logic in CS3_I_NHGAN_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_NHGAN')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/NHGAN_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
            df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 4410
    df_area_capacity.loc[df_area_capacity['Area'] > 4410, 'Area'] = 4410

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [317.123, 4410]

    # calculate and set the evaporation
    df_storage_data['OHGAN_evap'] = calculate_evap_data(df_storage_data['OHGAN_STORAGE'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_JNKSN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Jenkinson Reservoir. Follows the logic in CS3_I_CMP001_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_JNKSN')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/JNKSN_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(
        1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity[
        'Capacity (acre-feet)']) / (
                                       df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 650
    df_area_capacity.loc[df_area_capacity['Area'] > 650, 'Area'] = 650

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [41.4, 650]

    # calculate and set the evaporation
    df_storage_data['JNKSN_evap'] = calculate_evap_data(df_storage_data['JNKSN_STORAGE'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_JKSMD_I_NFY029(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Jackson Meadows Reservoir. Follows the logic in CS3_I_NFY029_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_JKSMD from 'CS3_ER_JKSMD_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_JKSMD')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/JKSMD_AC_I_NFY029.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    # the sheet gets the averages for each neighboring set of points and uses those
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
    df_area_capacity['Area'] = (
        df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']
    ) / (
        df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)']
    )

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure none of the areas are above a maximum of 938
    df_area_capacity.loc[df_area_capacity['Area'] > 938, 'Area'] = 938

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [71.0, 938]

    # calculate and set the evaporation
    df_storage_data['JKSMD_evap_I_NFY029'] = calculate_evap_data(df_storage_data.loc[:, "11407800_I_NFY029"], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_JKSMD(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Jackson Meadows Reservoir. Follows the logic in CS3_I_JKSMD_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_JKSMD from 'CS3_ER_JKSMD_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_JKSMD')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/JKSMD_AC.csv")

    # the sheet already has TAF
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['Storage (TAF)']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area already available
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # calculate and set the evaporation
    df_storage_data['JKSMD_evap'] = calculate_evap_data(df_storage_data.loc[:, "11407800"], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_BOWMN(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Bowman Lake. Follows the logic in CS3_I_BOWMN_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_BOWMN from 'CS3_ER_BOWMN_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BOWMN')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/BOWMN_AC.csv")

    # the sheet already has TAF
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['Storage (TAF)']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area already available
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # calculate and set the evaporation
    df_storage_data['BOWMN_evap'] = calculate_evap_data(df_storage_data.loc[:, "11415500"], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_FRNCH(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for French Lake. Follows the logic in CS3_I_BOWMN_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_FRNCH from 'CS3_ER_FRNCH_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FRNCH')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/FRNCH_AC.csv")

    # the sheet already has TAF
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['Storage (TAF)']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area already available
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # calculate and set the evaporation
    df_storage_data['FRNCH_evap'] = calculate_evap_data(df_storage_data.loc[:, "11414400_I_FRNCH"], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_FRDYC(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Fordyce Lake. Follows the logic in CS3_I_FRDYC_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_FRDYC from 'CS3_ER_FRDYC_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FRDYC')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/FRDYC_AC.csv")

    # the sheet already has TAF
    df_area_capacity['Elevation'] = df_area_capacity['Elevation (ft)']
    df_area_capacity['Capacity'] = df_area_capacity['Storage (TAF)']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area already available
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # calculate and set the evaporation
    df_storage_data['FRDYC_evap'] = calculate_evap_data(df_storage_data.loc[:, "11414090"], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_RLLNS(s_dss_file, df_storage_data, s_data_suffix=""):
    """
    Calculate the evaporation amount for Rollins Reservoir. Follows the logic in CS3_I_RLLNS_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_RLLNS from 'CS3_ER_RLLNS_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    s_data_suffix: str
        Suffix to add while accessing data (if there is duplicate data for the storage)

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_RLLNS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/RLLNS_AC.csv")
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()
    df_storage_data.loc[:, f'RLLNS_evap{s_data_suffix}'] = calculate_evap_data(
        df_storage_data.loc[:, f"11421800{s_data_suffix}"],
        df_evap_rates,
        df_area_capacity[['Capacity', 'Area']],
        b_set_zeros=True
    )


def calc_evap_CMBIE(s_dss_file, df_storage_data, s_data_suffix=""):
    """
    Calculate the evaporation amount for Combie Reservoir. Follows the logic in CS3_I_CMBIE_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_CMBIE from 'CS3_ER_CMBIE_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    s_data_suffix: str
        Suffix to add while accessing data (if there is duplicate data for the storage)

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_CMBIE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/CMBIE_AC.csv")
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [5.555, 360]
    # calculate_Evap_data function uses np.interp which can only
    # interpolate between the min and max, because the observed values
    # goes beyond 5.555, adding this row here for extrapolation using the
    # last 2 rows like excel
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [9, 635.7075]
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()
    df_storage_data.loc[:, f'CMBIE_evap{s_data_suffix}'] = calculate_evap_data(
        df_storage_data.loc[:, f"LAKE_COMBIE{s_data_suffix}"],
        df_evap_rates,
        df_area_capacity[['Capacity', 'Area']],
        b_set_zeros=False
    )


def calc_evap_CMPFW(s_dss_file, df_storage_data, s_data_suffix=""):
    """
    Calculate the evaporation amount for Camp Far West Reservoir. Follows the logic in CS3_I_CMBIE_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_CMPFW from 'CS3_ER_CMPFW_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    s_data_suffix: str
        Suffix to add while accessing data (if there is duplicate data for the storage)

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_CMPFW')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/CMPFW_AC.csv")
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    df_area_capacity.loc[len(df_area_capacity)-1, ['Capacity', 'Area']] = [125.0, 2050]
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()
    df_storage_data.loc[:, f'CMPFW_evap{s_data_suffix}'] = calculate_evap_data(
        df_storage_data.loc[:, f"CAMP_FAR{s_data_suffix}"],
        df_evap_rates,
        df_area_capacity[['Capacity', 'Area']],
        b_set_zeros=True
    )


def calc_evap_MERLC(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Lake Merle Collins. Follows the logic in CS3_I_MERLC_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_MERLC from 'CS3_ER_MERLC_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_MERLC')
    # get the storage for Lake Merle
    df_stor_MCollins = df_storage_data.loc[:, "LAKE_MERLE"]

    # TODO: do we need to run the curve filling here?
    # equation comes from excel
    # y = -0.00226x2 + 16.80972x - 1.51461
    df_evap_MCollins = (-0.00226 * df_stor_MCollins.pow(2) + 16.80972 * df_stor_MCollins - 1.51461) * df_evap_rates.loc[:, "IN"] / 12 / 1000
    df_storage_data.loc[:, f'MERLC_evap'] = df_evap_MCollins


def calc_evap_SPLDG(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Lake Spaulding. Follows the logic in CS3_I_CMBIE_Rev2022G. Updated to WY21 using calibrated evaporation rate ER_SPLDG from 'CS3_ER_SPLDG_rev1.xls

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir

    Returns
    -------
    None
    """

    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SPLDG')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/SPLDG_AC.csv")
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)
    df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
                df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # this one has different formula than others in the table
    df_area_capacity.loc[1, "Area"] = 20
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()
    df_storage_data.loc[:, f'SPLDG_evap'] = calculate_evap_data(
        df_storage_data.loc[:, "11414140"],
        df_evap_rates,
        df_area_capacity[['Capacity', 'Area']],
        b_set_zeros=True
    )
