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
            # linearly interpolate the capacities to get the area value for the current capacity. units are acres here
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

def calc_evap_11295900(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Pine Crest Reservoir. Follows the logic in CS3_I_SFS033_Rev2022F.

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_PCRST')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11295900_AC.csv")

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

    # make sure none of the areas are above a maximum of 300
    df_area_capacity.loc[df_area_capacity['Area'] > 300, 'Area'] = 300

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [18.6, 300]

    # calculate and set the evaporation
    df_storage_data['11295900_evap'] = calculate_evap_data(df_storage_data['11295900_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11297700(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Lyons Reservoir. Follows the logic in CS3_I_SFS030_Rev2022F.

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LYONS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11297700_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 170, 'Area'] = 170

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [6.3, 170]

    # calculate and set the evaporation
    df_storage_data['11297700_evap'] = calculate_evap_data(df_storage_data['11297700_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293460(s_dss_file, df_storage_data, b_use_old_evap):
    """
    Calculate the evaporation amount for Alpine Reservoir. Follows the logic in CS3_I_NFS033_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.
    Returns
    -------
    None
    """
    # get the evap rates from the dss file. Note this reservoir uses the Spicer Meadow Evaporation rate but everything
    # else pertains to this reservoir, not Spicer Meadow
    if b_use_old_evap:
        df_evap_rates = df_storage_data[['11293770_evap_rate']].copy()
        df_evap_rates.rename(columns={'11293770_evap_rate': 'IN'}, inplace=True)
    else:
        df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293460_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 179, 'Area'] = 179

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [4.3, 179]

    # calculate and set the evaporation
    df_storage_data['11293460_evap'] = calculate_evap_data(df_storage_data['11293460_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293460_v2(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Alpine Reservoir. Follows the logic in CS3_I_SPICE_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.
    Returns
    -------
    None
    """
    # get the evap rates from the dss file. Note this reservoir uses the Spicer Meadow Evaporation rate but everything
    # else pertains to this reservoir, not Spicer Meadow
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293460_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 179, 'Area'] = 179

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [4.3, 179]

    # calculate and set the evaporation
    df_storage_data['11293460_evap_v2'] = calculate_evap_data(df_storage_data['11293460_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293350(s_dss_file, df_storage_data, b_use_old_evap):
    """
    Calculate the evaporation amount for Union Reservoir. Follows the logic in CS3_I_NFS033_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    # get the evap rates from the dss file or csv file. Note this reservoir uses the Spicer Meadow Evaporation rate but everything
    # else pertains to this reservoir, not Spicer Meadow
    if b_use_old_evap:
        df_evap_rates = df_storage_data[['11293770_evap_rate']].copy()
        df_evap_rates.rename(columns={'11293770_evap_rate': 'IN'}, inplace=True)
    else:
        df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')
    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293350_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 197, 'Area'] = 197

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [3.3, 197]

    # calculate and set the evaporation
    df_storage_data['11293350_evap'] = calculate_evap_data(df_storage_data['11293350_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293350_v2(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Union Reservoir. Follows the logic in CS3_I_SPICE_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    # get the evap rates from the dss file or csv file. Note this reservoir uses the Spicer Meadow Evaporation rate but everything
    # else pertains to this reservoir, not Spicer Meadow
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')
    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293350_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 197, 'Area'] = 197

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [3.3, 197]

    # calculate and set the evaporation
    df_storage_data['11293350_evap_v2'] = calculate_evap_data(df_storage_data['11293350_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_11293370(s_dss_file, df_storage_data, b_use_old_evap):
    """
    Calculate the evaporation amount for Utica Reservoir. Follows the logic in CS3_I_NFS033_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    # get the evap rates from the dss file or csv file. Note this reservoir uses the Spicer Meadow Evaporation rate but everything
    # else pertains to this reservoir, not Spicer Meadow
    if b_use_old_evap:
        df_evap_rates = df_storage_data[['11293770_evap_rate']].copy()
        df_evap_rates.rename(columns={'11293770_evap_rate': 'IN'}, inplace=True)
    else:
        df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')
    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293370_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 250, 'Area'] = 250

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [2.6, 250]

    # calculate and set the evaporation
    df_storage_data['11293370_evap'] = calculate_evap_data(df_storage_data['11293370_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293370_v2(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Utica Reservoir. Follows the logic in CS3_I_SPICE_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')
    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293370_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 250, 'Area'] = 250

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [2.6, 250]

    # calculate and set the evaporation
    df_storage_data['11293370_evap_v2'] = calculate_evap_data(df_storage_data['11293370_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293770(s_dss_file, df_storage_data, b_use_old_evap):
    """
    Calculate the evaporation amount for Spicer Meadow Reservoir. Follows the logic in CS3_I_NFS033_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    # get the evap rates from the dss file or csv file
    if b_use_old_evap:
        df_evap_rates = df_storage_data[['11293770_evap_rate']].copy()
        df_evap_rates.rename(columns={'11293770_evap_rate': 'IN'}, inplace=True)
    else:
        df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293770_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 1998, 'Area'] = 1998

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [189.7, 1998]

    # calculate and set the evaporation
    df_storage_data['11293770_evap'] = calculate_evap_data(df_storage_data['11293770_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11293770_v2(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Spicer Meadow Reservoir. Follows the logic in CS3_I_SPICE_Rev2022G.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_use_old_evap: bool
        Flag to use an older version of the Spicer Evap rate to replicate the 2021 extension in the sheets.

    Returns
    -------
    None
    """
    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SPICE')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11293770_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 1998, 'Area'] = 1998

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [189.7, 1998]

    # calculate and set the evaporation
    df_storage_data['11293770_evap_v2'] = calculate_evap_data(df_storage_data['11293770_filled'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_11291000(s_dss_file, df_storage_data, b_replicate):
    """
    Calculate the evaporation amount for Relief Reservoir. Follows the logic in CS3_I_RLIEF_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_replicate: bool
        A flag to replicate sheets, in this case storage values from an unknown data source.
    Returns
    -------
    None
    """
    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_RLIEF')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11291000_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 401, 'Area'] = 401

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [64.9, 401]

    # calculate and set the evaporation
    if b_replicate:
        df_storage_data['11291000_evap'] = calculate_evap_data(df_storage_data['RLF_REPLICATION'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)
    else:
        df_storage_data['11291000_evap'] = calculate_evap_data(df_storage_data['11291000_filled_2'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11291000_v2(s_dss_file, df_storage_data, b_replicate):
    """
    Calculate the evaporation amount for Relief Reservoir including a unit coversion error. Follows the logic in CS3_I_BEARD_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_replicate: bool
        A flag to replicate sheets, in this case storage values from an unknown data source.
    Returns
    -------
    None
    """
    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_RLIEF')

    # reproduce unit-conversion error in CS3_I_BEARD_Rev2022F sheet "Relief Evaporation" Column D, where the formula
    # should end with 1000) instead of 12000)
    df_evap_rates = df_evap_rates / 12.0

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11291000_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 401, 'Area'] = 401

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [64.9, 401]

    # calculate and set the evaporation
    if b_replicate:
        df_storage_data['11291000_evap_v2'] = calculate_evap_data(df_storage_data['RLF_REPLICATION'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)
    else:
        df_storage_data['11291000_evap_v2'] = calculate_evap_data(df_storage_data['11291000_filled_2'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_11292600(s_dss_file, df_storage_data, b_replicate):
    """
    Calculate the evaporation amount for Donnell Reservoir. Follows the logic in CS3_I_DONLL_Rev2022F.

    Parameters
    ----------
    s_dss_file: str
        Path to DSS file with evaporation rates
    df_storage_data: dataframe
        Storage data containing the reservoir
    b_replicate: bool
        A flag to replicate sheets, in this case storage values from an unknown data source.
    Returns
    -------
    None
    """
    # get the evap rates from the dss file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_DONLL')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11292600_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 401, 'Area'] = 401

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [64.9, 401]

    # calculate and set the evaporation
    df_storage_data['11292600_evap'] = calculate_evap_data(df_storage_data['11292600'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11292800(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for Beardsley Reservoir. Follows the logic in CS3_I_BEARD_Rev2022G.

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BEARD')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11292800_AC.csv")

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

    # make sure none of the areas are above the maximum
    df_area_capacity.loc[df_area_capacity['Area'] > 650, 'Area'] = 650

    # make sure the areas are monotonically increasing
    df_area_capacity["Area"] = df_area_capacity["Area"].cummax()

    # add a row for the maximum
    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [98.5, 650]

    # calculate and set the evaporation
    df_storage_data['11292800_evap'] = calculate_evap_data(df_storage_data['11292800'], df_evap_rates,
                                                        df_area_capacity[['Capacity', 'Area']], True)
