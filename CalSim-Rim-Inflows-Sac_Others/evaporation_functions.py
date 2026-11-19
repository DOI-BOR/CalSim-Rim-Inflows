######################################################
#### DWR MSO OFFICE                                ###
#### Calsim Data Extention - Rim Watershed Project ###
#### Region : "Sacramento Other"                   ###
#####################################################################################################################
## Rim Inflow:                                                                                                    ###
## I_SHSTA  : Lake Shasta            #I_COW014 : No Storage                    #I_BCN010 : No Storage             ###
## I_BTL006 : No Storage             #I_PYN001 : No Storage                    #I_ANT011 : No Storage             ###
## I_MNS000 : No Storage             #I_TRNTY  : Lake Trinity                  #I_WKYTN  : WHISKEYTOWN RESERVOIR  ###
## I_SCW008 : No Storage             #I_ELD027 : No Storage                    #I_THM028 : No Storage             ###
## I_BLKBT  : No Storage             #I_SGRGE  : No Storage                    #I_EPARK  : No Storage             ###
## I_INDVL  : INDIAN VALLEY          #I_CCH053 : Lake BERRYESSA                #I_PTH070 : Lake BERRYESSA         ###                      
## I_LWSTN  : Lake Lewiston          #I_CLR011 : WHISKEYTOWN RESERVOIR         #I_CWD018 : No Storage             ###
## I_BCC014 : No Storage             #I_BTC048 : No Storage                    #I_LCC038 : No Storage             ###
## I_CLRLK  : Clear Lake             #I_BRC003 : Lake BERRYESSA                #I_LDC029 : No Storage             ###
## I_HON021 : No Storage             #I_MLC006 : No Storage                    #I_DRC012 : No Storage             ###
#####################################################################################################################

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
            d_pred_area = np.interp(row['Averages'], df_area_capacity['Capacity'], df_area_capacity['Area'])

            # multiply but the evap rate
            df_evaporation_data.loc[index, 'TAF'] = d_pred_area * df_evap_rates.loc[index, 'Feet'] / 1000

    # return the dataframe
    return df_evaporation_data.copy()



def calc_evap_SHA(s_dss_file, df_storage_data):  #Calculates the evaporation amount for lake Shasta Resevoir
  
    ### NOTE : Evap Rate in DSS file does not match Excel (DSS file has been updated)
       
    df_evap_rates = read_evap_data(s_dss_file, 'ER_SHSTA') 
    df_area_capacity = pd.DataFrame()
    df_area_capacity['Capacity'] = df_storage_data['SHA']
    df_area_capacity['Area'] = -0.0006*df_storage_data['SHA']**2 + 9.2406*df_storage_data['SHA'] + 1416.8
    # calculate and set the evaporation
    df_storage_data['SHA_evap'] = (df_evap_rates.iloc[:, 0] * df_area_capacity['Area'] ) / (12 * 1000)


def calc_evap_CLE(s_dss_file, df_storage_data):   #Calculates the evaporation amount for Trinity Storage
  
    # Note : No calculation neede.  data comes from Cdec directly- extend Trinity Storage Evap using CDEC(CLE) in  Lake-Trinity_AC.csv
  
    df_area_capacity = pd.read_csv("./Inputs/Area_Capacities/Lake-Trinity_AC.csv",index_col="date")
    df_area_capacity.index = pd.to_datetime(df_area_capacity.index)
    df_area_capacity['TAF'] = df_area_capacity['CLE-evap (acre-feet)'] / 1000
    # calculate and set the evaporation
    df_storage_data["CLE_evap"] = df_area_capacity['TAF'] 

def calc_evap_LEW(s_dss_file, df_storage_data):    # Calculates the evaporation amount for Lewiston-Storage
   
    df_evap_rates = read_evap_data(s_dss_file, 'ER_LWSTN') 
    df_area_capacity = pd.DataFrame()
    df_area_capacity['Capacity'] = df_storage_data['LEW']
    df_area_capacity['Area'] = -1.9151*df_storage_data['LEW']**2 + 78.909*df_storage_data['LEW'] + 9.9285
    # calculate and set the evaporation
    df_storage_data['LEW_evap'] = (df_evap_rates.iloc[:, 0] * df_area_capacity['Area'] ) / (12 * 1000)

    
def calc_evap_WHI(s_dss_file, df_storage_data):  # Calculates the evaporation amount for WHISKEYTOWN RESERVOIR
     
    df_evap_rates = read_evap_data(s_dss_file, 'ER_WKYTN') 
    df_area_capacity = pd.DataFrame()
    df_area_capacity['Capacity'] = df_storage_data['WHI']
    df_area_capacity['Area'] = -0.0298*df_storage_data['WHI']**2 + 19.785*df_storage_data['WHI'] + 167.71
    # calculate and set the evaporation
    df_storage_data['WHI_evap'] = (df_evap_rates.iloc[:, 0] * df_area_capacity['Area'] ) / (12 * 1000)
       
def calc_evap_CLAKE(s_dss_file, df_storage_data):   # Calculates the evaporation amount for Clear Lake

    # NOTE : No calcvulation data come from source directly - extend ClearLake ET using in  ClearLake_AC.csv ((combination of differen tDataaset))
 
    df_evap_rates = read_evap_data(s_dss_file, 'ER_CLRLK')
    df_evap_rates['Feet'] = df_evap_rates['IN']/12
    df_area_capacity = pd.read_csv("./Inputs/Area_Capacities/ClearLake_AC.csv",index_col="date")
    df_area_capacity.index = pd.to_datetime(df_area_capacity.index)
    df_area_capacity['Area'] = df_area_capacity['Area (acres)'] 
    # calculate and set the evaporation
    df_storage_data["11451000_evap"] = (df_area_capacity['Area'] * df_evap_rates['Feet'])/1000
      
    
def calc_evap_BRY(s_dss_file, df_storage_data):   # Calculates the evaporation amount for LAKE_BERRYESSA
   
    # NOTE : No calculation data come from csv file - from 1975 to 2009 data doesnot follow area-capacity equation in excel sheet
    # data direcly being read from csv file
    df_evap_rates = read_evap_data(s_dss_file, 'ER_BRYSA')  # is not used
    df_area_capacity = pd.read_csv("./Inputs/Area_Capacities/bry_AC.csv",index_col="date")
    df_area_capacity.index = pd.to_datetime(df_area_capacity.index)
    df_area_capacity['TAF'] = df_area_capacity['bry-evap (acre-feet)'] /1000
    #calculate and set the evaporation
    df_storage_data["11453900_evap"] = df_area_capacity['TAF'] 
  
    
def calc_evap_INDVL(s_dss_file, df_storage_data):    # Calculates the evaporation amount for INDIAN VALLEY RESERVOIR EVAPORATION


    df_evap_rates = read_evap_data(s_dss_file, 'ER_INDVL') 
    df_area_capacity = pd.DataFrame()
    df_area_capacity['Capacity'] = df_storage_data['INV']
    df_area_capacity['Area'] = -6.60E-07*df_storage_data['INV']**4 + 5.41E-04*df_storage_data['INV']**3 + -1.763E-01*df_storage_data['INV']**2 + 35.4*df_storage_data['INV']
    # calculate and set the evaporation
    df_storage_data['INDVL_evap'] = (df_evap_rates.iloc[:, 0] * df_area_capacity['Area'] ) / (12 * 1000)
