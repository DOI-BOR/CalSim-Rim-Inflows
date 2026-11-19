import pandas as pd
import numpy as np
from extension_functions import create_final_flow_plots, area_scale, remove_negatives_timeseries
from datetime import datetime




def I_GZL009(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_GZL009

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11404300']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_GZL009'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1994, 2025)), 'I_GZL009')

def I_ALMNR(df_unimpaired_data, df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALMNR and I_MTMDW

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
      
    
    
    df_location= df_unimpaired_data['11399500']*0.76
    
    df_location[datetime(1921, 10, 31):datetime(1992,9,30)]= df_full_data['FPR'][datetime(1921, 10, 31):datetime(1992,9,30)]*0.76
    
    df_location[datetime(2016,10,30):datetime(2019, 9, 30)] = df_unimpaired_data['11401112'][datetime(2016,10,30):datetime(2019, 9, 30)]*0.64

    
       # round to two decimal places
    df_location = df_location.round(2)

     # add into the rim inflow dataframe
    df_rim_inflows['I_ALMNR'] = df_location
    
    
    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_ALMNR')

def I_MTMDW(df_unimpaired_data,df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALMNR and I_MTMDW

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
      
    
    
    df_location= df_full_data['FPR']*0.24
    
    df_location[datetime(1992, 10, 31):datetime(2021,9,30)]= df_unimpaired_data['11399500'][datetime(1992, 10, 31):datetime(2021,9,30)]*0.24
    
    df_location[datetime(2016,10,30):datetime(2019, 9, 30)] = df_unimpaired_data['11401112'][datetime(2016,10,30):datetime(2019, 9, 30)]*0.20

       # round to two decimal places
    df_location = df_location.round(2)

     # add into the rim inflow dataframe
    df_rim_inflows['I_MTMDW'] = df_location
    
    
    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_MTMDW')

def I_BTVLY(df_extended_data,df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_BTVLY

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_unimpaired_data['11400500']
    
    df_location[datetime(1921,10,31):datetime(1936,9,30)]= df_extended_data['11400500'][datetime(1921,10,31):datetime(1936,9,30)]
    df_location[datetime(2018,10,31):datetime(2019,9,30)]= df_extended_data['11400500'][datetime(2018,10,31):datetime(2019,9,30)]
    df_location[datetime(1936,10,31):datetime(1964,9,30)]= df_unimpaired_data['11400000'][datetime(1936,10,31):datetime(1964,9,30)]/0.995670996


    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_BTVLY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1965, 2025)), 'I_BTVLY')

def I_NFF058(df_extended_data,df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFF058

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_unimpaired_data['11401112'].copy()
    
    df_location[datetime(1921,10,31):datetime(1980,9,30)]= df_extended_data['11401112'][datetime(1921,10,31):datetime(1980,9,30)]
    df_location = df_location - df_rim_inflows['I_ALMNR'] - df_rim_inflows['I_MTMDW'] - df_rim_inflows['I_BTVLY']

    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    
    #print(df_location_positive[datetime(2014,10,31):datetime(2015,9,30)])

    # set anything negative to zero
    df_location_positive.loc[df_location_positive < 0] = 0

    # round to two decimal places
    df_location_positive = df_location_positive.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFF058'] = df_location_positive

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location_positive, list(range(1965, 2025)), 'I_NFF058')    

def I_ANTLP(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ANTLP

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['ANT_FNF'].copy()
    df_location[datetime(1930,10,31):datetime(1963,9,30)]= df_extended_data['11401125'][datetime(1930,10,31):datetime(1963,9,30)]
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ANTLP'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1994, 2025)), 'I_ANTLP')


def I_EBF001(df_extended_data, df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_GZL009

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11403000'].copy()
    df_location[datetime(1968,10,31):datetime(1982,9,30)]=df_unimpaired_data['11403000'][datetime(1968,10,31):datetime(1982,9,30)]
    df_location = df_location -df_rim_inflows['I_ANTLP']
   
    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_EBF001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1994, 2025)), 'I_EBF001')

def I_NFF046(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFF046

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11403200'].copy()
    df_location = df_location - df_rim_inflows['I_ALMNR'] - df_rim_inflows['I_MTMDW'] - df_rim_inflows['I_BTVLY'] - df_rim_inflows['I_NFF058']- df_rim_inflows['I_ANTLP'] -df_rim_inflows['I_EBF001'] 
        
    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    
    # set anything negative to zero
    df_location_positive.loc[df_location_positive < 0] = 0

    # round to two decimal places
    df_location_positive = df_location_positive.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFF046'] = df_location_positive

def I_UBUCK(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_BUCKS

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11403530'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied area ratio of 0.92
    df_rim_inflows['I_UBUCK'] = df_location*0.92

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_UBUCK')

def I_LBUCK(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LBUCK

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11403530'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied area ratio of 0.92
    df_rim_inflows['I_LBUCK'] = df_location*0.08

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_LBUCK')

def I_MLK003(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MLK003

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11403530'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied area ratio of 0.161
    df_rim_inflows['I_MLK003'] = df_location*0.161

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_MLK003')

def I_NFF029(df_unimpaired_data, df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFF029

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_full_data['FPL'].copy()+0.2*df_full_data['FTO_CU']
    df_location[datetime(1966,10,31):datetime(2021,9,30)]= df_unimpaired_data['11404500'][datetime(1966,10,31):datetime(2021,9,30)]

    df_location = df_location - df_rim_inflows['I_ALMNR'] - df_rim_inflows['I_MTMDW'] - df_rim_inflows['I_BTVLY'] - df_rim_inflows['I_NFF046']- df_rim_inflows['I_ANTLP'] -df_rim_inflows['I_EBF001']-df_rim_inflows['I_UBUCK']-df_rim_inflows['I_LBUCK']-df_rim_inflows['I_MLK003']-df_rim_inflows['I_GZL009']-df_rim_inflows['I_NFF058']

    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    
    #print(df_location_positive[datetime(2014,10,31):datetime(2015,9,30)])

    # set anything negative to zero
    df_location_positive.loc[df_location_positive < 0] = 0

    # round to two decimal places
    df_location_positive = df_location_positive.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFF029'] = df_location_positive    

def I_DAVIS(df_extended_data, df_unimpaired_data, df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DAVIS

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11391500'].copy()
    df_location[datetime(1925,10,31):datetime(1932,9,30)]=df_unimpaired_data['11391500'][datetime(1925,10,31):datetime(1932,9,30)]
    df_location[datetime(1950,10,31):datetime(1953,9,30)]=df_unimpaired_data['11391500'][datetime(1950,10,31):datetime(1953,9,30)]
    df_location[datetime(1954,10,31):datetime(1967,9,30)]=df_unimpaired_data['11391500'][datetime(1954,10,31):datetime(1967,9,30)]
    df_location[datetime(1966,12,31):datetime(2021,9,30)]=df_full_data['DAV_FNF'][datetime(1966,12,31):datetime(2021,9,30)]
   
    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_DAVIS'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1994, 2025)), 'I_DAVIS')


def I_FRMAN(df_extended_data, df_full_data,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFF058

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11391400'].copy()
    
    
    #df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    
    #print(df_location_positive[datetime(2014,10,31):datetime(2015,9,30)])

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_FRMAN'] = df_location
    df_rim_inflows['I_FRMAN'][datetime(1965,1,31):datetime(2021,9,30)]= df_full_data['FRD_FNF'] [datetime(1965,1,31):datetime(2021,9,30)]

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2025)), 'I_FRMAN')    

def I_MFF087(df_unimpaired_data, df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFF087

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_11394500 =df_full_data['FTM']+0.8*df_full_data['FTO_CU']-df_full_data['FTT']
    
    df_11394500[datetime(1952,10,31):datetime(2021,9,30)]=df_unimpaired_data['11394500_A'][datetime(1952,10,31):datetime(2021,9,30)]

    df_location=df_11394500 *0.210
    df_location[datetime(1968,10,31):datetime(1976,9,30)]=df_unimpaired_data['11392100'][datetime(1968,10,31):datetime(1976,9,30)]
    df_location[datetime(1977,10,31):datetime(1980,9,30)]=df_unimpaired_data['11392100'][datetime(1977,10,31):datetime(1980,9,30)]
    df_location = df_location - df_rim_inflows['I_DAVIS'] - df_rim_inflows['I_FRMAN']
    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # set anything negative to zero
    df_location_positive.loc[df_location_positive < 0] = 0

    # round to two decimal places
    df_location_positive = df_location_positive.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFF087'] = df_location_positive

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location_positive, list(range(1994, 2025)), 'I_MFF087')

def I_MFF019(df_unimpaired_data, df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFF087

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_11394500 =df_full_data['FTM']+0.8*df_full_data['FTO_CU']-df_full_data['FTT']
    
    df_11394500[datetime(1952,10,31):datetime(2021,9,30)]=df_unimpaired_data['11394500_A'][datetime(1952,10,31):datetime(2021,9,30)]

    df_location=df_11394500 - df_rim_inflows['I_DAVIS'] - df_rim_inflows['I_FRMAN'] -df_rim_inflows['I_MFF087']
    
    
    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFF019'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1994, 2025)), 'I_MFF019')

def I_WBF006(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_WBF006

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11406500'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied precipitation volume ratio of 0.2074
    df_rim_inflows['I_WBF006'] = df_location*0.2074

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_WBF006')

def I_WBF015(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_WBF015

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11406500'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied precipitation volumne ratio of 0.443
    df_rim_inflows['I_WBF015'] = df_location*0.443

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_WBF015')

def I_WBF030(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_WBF030

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11406500'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied precipitation volumne ratio of 0.2884
    df_rim_inflows['I_WBF030'] = df_location*0.2884

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_WBF030')

def I_LGRSV(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LGRSV

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11395030']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LGRSV'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location,  list(range(1922, 2025)), 'I_LGRSV')   

def I_SLYCK(df_extended_data, df_rim_inflows, df_synthetic_data):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLYCK

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11396000']
    df_location[datetime(1921,10,31):datetime(1973,9,30)]= df_synthetic_data['11396000'][datetime(1921,10,31):datetime(1973,9,30)]
    df_location = df_location * 24 /30

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLYCK'] = df_location 

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SLYCK')

def I_LSTCK(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LSTCK

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    df_location = df_rim_inflows['I_SLYCK'] * (6 / 24)
   

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LSTCK'] = df_location 

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_LSTCK')

def I_SFF029(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFF029

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # pull out the relevant station
    df_location = df_extended_data['11395200']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_LGRSV']

    # redistribute negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']


    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFF029'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2021)), 'I_SFF029')

def I_SFF019(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFF019

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # pull out the relevant station
    df_location = df_extended_data['11397000']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_LGRSV'] - df_rim_inflows['I_SLYCK'] - df_rim_inflows['I_LSTCK'] - df_rim_inflows['I_SFF029']
    df_location = df_location * (87.5-37.7-30) / (134-37.7-30)
    
    # redistribute negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']


    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFF019'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SFF019') 

def I_SFF011(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFF011

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # pull out the relevant station
    df_location = df_extended_data['11397000']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_LGRSV'] - df_rim_inflows['I_SLYCK'] - df_rim_inflows['I_SFF029'] - df_rim_inflows['I_LSTCK']
    df_location = df_location * (108-87.5)/(134-37.7-30)

    # redistribute negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']


    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFF011'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SFF011')     

def I_RVPHB(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RVPHB

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of extended (and unimpaired where relevant) data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_extended_data['11406500'].copy()
    
        # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe multiplied precipitation volumne ratio of 0.0612
    df_rim_inflows['I_RVPHB'] = df_location*0.0612

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1999, 2025)), 'I_RVPHB')

def I_OROVL(df_full_data, df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_FOLSM

    Parameters
    ----------
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_unimpaired_data: dataframe
        Dataframe of unimpaired flows
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['Unimpaired_ORO'] - df_rim_inflows['I_ALMNR'] - df_rim_inflows['I_ANTLP'] - df_rim_inflows['I_BTVLY'] - df_rim_inflows['I_DAVIS'] - df_rim_inflows['I_EBF001']
    df_location = df_location- df_rim_inflows['I_FRMAN'] - df_rim_inflows['I_GZL009'] - df_rim_inflows['I_LBUCK'] - df_rim_inflows['I_UBUCK'] - df_rim_inflows['I_LGRSV']
    df_location = df_location- df_rim_inflows['I_LSTCK'] - df_rim_inflows['I_MFF019'] - df_rim_inflows['I_MFF087'] - df_rim_inflows['I_MLK003'] - df_rim_inflows['I_MTMDW']
    df_location = df_location- df_rim_inflows['I_NFF029'] - df_rim_inflows['I_NFF046'] - df_rim_inflows['I_NFF058'] - df_rim_inflows['I_RVPHB'] - df_rim_inflows['I_SFF011']-df_rim_inflows['I_SFF019']
    df_location = df_location- df_rim_inflows['I_SFF029'] - df_rim_inflows['I_SLYCK'] - df_rim_inflows['I_WBF006'] - df_rim_inflows['I_WBF015'] - df_rim_inflows['I_WBF030']
    #df_rim_inflows[['I_ALMNR', 'I_ANTLP','I_BTVLY', 'I_DAVIS',  'I_EBF001', 'I_FRMAN','I_GZL009', 'I_LBUCK','I_UBUCK', 'I_LGRSV', 'I_LSTCK', 'I_MFF019',
    #                                                       'I_MFF087',  'I_MLK003', 'I_MTMDW','I_NFF029', 'I_NFF046', 'I_NFF058', 'I_RVPHB','I_SFF011', 'I_SFF019', 'I_SFF029', 'I_SLYCK', 'I_WBF006',
    #                                                        'I_WBF015',  'I_WBF030']].sum(axis=1)

    
    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_OROVL'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_OROVL')