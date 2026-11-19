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
            # linearly interpolate the capacities to get the area value for the current capacity. units are acers here
            # d_pred_area = np.interp(row['Averages'], df_area_capacity['Capacity'], df_area_capacity['Area'])
            d_pred_area = np.interp(row['Averages'], df_area_capacity['Capacity'], df_area_capacity['Area'])
            
            # multiply but the evap rate
            df_evaporation_data.loc[index, 'TAF'] = d_pred_area * df_evap_rates.loc[index, 'Feet'] / 1000
            
    # return the dataframe
    return df_evaporation_data.copy()



def calc_evap_FRD(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC FRD Frenchman RESERVOIR (Frenchman DAM). Follows the logic in CS3_I_FRMAN_Rev2022G

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_FRMAN')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/FRD_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # make sure none of the areas are above a maximum of 2252
    df_area_capacity.loc[df_area_capacity['Area'] > 2252, 'Area'] = 2252

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [91.708, 2252]

    # calculate and set the evaporation
    df_storage_data['FRD_evap'] = calculate_evap_data(df_storage_data['FRD'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)
    
def calc_evap_11404250(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11404250 GRIZZLY FOREBAY NR STORRIE CA. Follows the logic in CS3_I_GZL009_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BUCKS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11404250_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # make sure none of the areas are above a maximum of 38
    df_area_capacity.loc[df_area_capacity['Area'] > 38, 'Area'] = 38

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [1.112, 38]

    # calculate and set the evaporation
    df_storage_data['11404250_evap'] = calculate_evap_data(df_storage_data['11404250'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True) 

def calc_evap_MMW(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC MMW MOUNTAIN MEADOWS RESERVOIR. Follows the logic in CS3_I_MTMDW_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_MTMDW')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/MMW_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']

    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 5702.857143, 'Area'] = 5702.857143

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [23.952, 5702.857143]

    # calculate and set the evaporation
    df_storage_data['MMW_evap'] = calculate_evap_data(df_storage_data['MMW'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)
    df_storage_data['MMW_EX_evap'] = calculate_evap_data(df_storage_data['MMW_EX'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)
    
def calc_evap_11399000(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGA 11399000 LAKE ALMANOR A PRATTVILLE CA. Follows the logic in CS3_I_ALMNR_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_ALMNR')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11399000_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 28400, 'Area'] = 28400

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [1185.4756, 28400]

    # calculate and set the evaporation
    df_storage_data['11399000_evap'] = calculate_evap_data(df_storage_data['11399000'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_BTV(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC BTV BUTT VALLEY RESERVOIR STORAGE . Follows the logic in CS3_I_BTVLY_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BTVLY')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/BTV_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 1614.286, 'Area'] = 1614.286

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [52.241, 1614.286]

    # calculate and set the evaporation
    df_storage_data['BTV_evap'] = calculate_evap_data(df_storage_data['BTV'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_ANT(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC ANT ANTELOPE LAKE STORAGE . Follows the logic in CS3_I_BTVLY_ANTLP2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_ANTLP')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/ANT_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 931, 'Area'] = 931

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [25, 931]

    # calculate and set the evaporation
    df_storage_data['ANT_evap'] = calculate_evap_data(df_storage_data['ANT'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11403500(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11403500 BUCKS Lake Near BUCKS LODGE CA  . Follows the logic in CS3_I_UBUCK_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BUCKS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11403500_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 1817, 'Area'] = 1817

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [105.5, 1817]

    # calculate and set the evaporation
    df_storage_data['11403500_evap'] = calculate_evap_data(df_storage_data['11403500'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)


def calc_evap_11403520(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for USGS 11403520 LOW BUCKS LAKE NEAR BUCKS LODGE CA  . Follows the logic in CS3_I_UBUCK_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BUCKS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11403520_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 136, 'Area'] = 136

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [6.3, 136]

    # calculate and set the evaporation
    df_storage_data['11403520_evap'] = calculate_evap_data(df_storage_data['11403520'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_DAV(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for CDEC DAV, LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM) . Follows the logic in CS3_I_DAVIS_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_DAVIS')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/DAV_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 4026, 'Area'] = 4026

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [91.3, 4026]

    # calculate and set the evaporation
    df_storage_data['DAV_evap'] = calculate_evap_data(df_storage_data['DAV'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_RVPHB(s_dss_file, df_storage_data):
    """
    Calculate the evaporation amount for  . Follows the logic in CS3_I_WBF006_Rev2025

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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_RVPHB')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/RVPHB_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Storage (TAF)']

    # the sheet just uses the provided values
    df_area_capacity['Capacity'] = df_area_capacity['TAF']
    df_area_capacity['Area'] = df_area_capacity['Area (acres)']
    
    # make sure none of the areas are above a maximum of 28400
    df_area_capacity.loc[df_area_capacity['Area'] > 261.1196, 'Area'] = 261.1196

    df_area_capacity.loc[len(df_area_capacity), ['Capacity', 'Area']] = [6.26, 261.1196]

    # calculate and set the evaporation
    df_storage_data['RVPHB_evap'] = calculate_evap_data(df_storage_data['S_RVPHB'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], True)

def calc_evap_11395020(s_dss_file, df_storage_data):
    """
    Calculates the evaporation amount for USGS 11395020 LITTLE GRASS VALLEY RESERVOIR NEAR LA PORTE, CA
    
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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LGRSV')

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11395020_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    #df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    df_area_capacity['Capacity'] = df_area_capacity['TAF']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
   # df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
          #      df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity['Area'] = df_area_capacity["Area (acres)"]
    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11395020_evap'] = calculate_evap_data(df_storage_data['11395020'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)


def calc_evap_11395400(s_dss_file, df_storage_data):
    """
    Calculates the evaporation amount for USGS 11395400 SLY CREEK RESERVOIR
    
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
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SLYCK')  #updated exisiting rates to match spreadsheet rates
    #df_evap_rates = pd.read_csv( "./Inputs/Evap_rates_temp.csv", index_col=0, parse_dates=True) #temp fix to match the spreadsheet rates because spreadsheet and dss rates differ. need to confirm which one to use.
    #df_evap_rates = df_evap_rates[["ER_SLYCK"]].rename(columns={"ER_SLYCK": "IN"})

    # read in the area capacity table
    df_area_capacity = pd.read_csv(r"./Area Capacities/11395400_AC.csv")

    # get the TAF capacity
    df_area_capacity['TAF'] = df_area_capacity['Capacity (acre-feet)'] / 1000

     # the sheet gets the averages for each neighboring set of points (mid-point elevation and capacity) and uses those, not sure why, but we will replicate
    df_area_capacity['Elevation'] = (df_area_capacity['Elevation (ft)'] + df_area_capacity['Elevation (ft)'].shift(1)) / 2
    df_area_capacity['Capacity'] = (df_area_capacity['TAF'] + df_area_capacity['TAF'].shift(1)) / 2
    #df_area_capacity['Capacity'] = df_area_capacity['TAF']

    # fill NAs with zero as the sheet does, this will populate the first row
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # area = diff in capacity/ diff in elevation (ac-ft/ft=ac)
   # df_area_capacity['Area'] = (df_area_capacity['Capacity (acre-feet)'].shift(1) - df_area_capacity['Capacity (acre-feet)']) / (
          #      df_area_capacity['Elevation (ft)'].shift(1) - df_area_capacity['Elevation (ft)'])
    df_area_capacity['Area'] = df_area_capacity["Area (acres)"]
    # again fill first row (lowest elevation) with zeros
    df_area_capacity.iloc[0, :] = df_area_capacity.iloc[0].fillna(0)

    # calculate and set the evaporation
    df_storage_data['11395400_evap'] = calculate_evap_data(df_storage_data['11395400'], df_evap_rates, df_area_capacity[['Capacity', 'Area']], b_set_zeros=True)