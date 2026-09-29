import pandas as pd
import numpy as np
from extension_functions import create_final_flow_plots, area_scale, remove_negatives_timeseries, unimpaired_flows
from datetime import datetime

def I_DCC010(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DCC010

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
    df_location = df_extended_data['11427700']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_DCC010'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1961, 2025)), 'I_DCC010')


def I_FRMDW(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_FRMDW

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
    df_location = df_extended_data['11427500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_FRMDW'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2024)), 'I_FRMDW')


def I_MFA036(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA036

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
    df_location = df_extended_data['11427760']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_FRMDW'] - df_rim_inflows['I_DCC010']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA036'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)), 'I_MFA036')


def I_RUB047(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RUB047

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
    df_location = df_extended_data['11428000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_RUB047'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1957, 1987)), 'I_RUB047')


def I_LRB004(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LRB004

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
    df_location = df_extended_data['11428400']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LRB004'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1991, 2016)), 'I_LRB004')


def I_HHOLE(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_HHOLE

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
    df_location = df_extended_data['11428800']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_HHOLE'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 2008)) + list(range(2009, 2025)), 'I_HHOLE')


def I_LOONL(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LOONL

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
    df_location = df_extended_data['11429500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LOONL'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2025)), 'I_LOONL')


def I_SFA066(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA066

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
    df_location = df_extended_data['11439501']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_CAPLS'] - df_rim_inflows['I_SILVR'] - df_rim_inflows['I_ALOHA'] - df_rim_inflows['I_PYR001']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.443

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA066'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SFA066')


def I_SFR006(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFR006

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
    df_location = df_extended_data['11430000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.401

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFR006'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2022)), 'I_SFR006')


def I_GERLE(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_GERLE

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
    df_location = df_rim_inflows['I_SFR006']

    # scale it based on area change
    df_location = area_scale(df_location, d_area_1=0.599, d_area_2=0.401)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_GERLE'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1963, 2022)), 'I_GERLE')


def I_STMPY(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_STMPY

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
    df_location = df_extended_data['11433040']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.716

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_STMPY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1962, 2018)) + list(range(2019, 2025)), 'I_STMPY')


def I_PLC007(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_PLC007

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
    df_location = df_extended_data['11433040']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # scaled by the water shed factors
    df_location = df_location * 0.284

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_PLC007'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1962, 2018)) + list(range(2019, 2025)), 'I_PLC007')


def I_NLC003(df_extended_data, df_gauge_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NLC003

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
    df_location = df_extended_data['11433100']

    # scaled by the water shed factors
    df_location = df_location * 0.15

    # we want the max of the scaled unimpaired data and this gauge location
    df_location = pd.concat([df_location, df_gauge_data['11433080']], axis=1).max(axis=1)

    # trim off the first date that gets added
    df_location = df_location.iloc[1:]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NLC003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_NLC003')

def I_SLC003(df_extended_data, df_gauge_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLC003

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
    df_location = df_extended_data['11433100']

    # scaled by the water shed factors
    df_location = df_location * 0.27

    # we want the max of the scaled unimpaired data and this gauge location
    df_location = pd.concat([df_location, df_gauge_data['11433060']], axis=1).max(axis=1)

    # trim off the first date that gets added
    df_location = df_location.iloc[1:]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLC003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_SLC003')


def I_LNG012(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LNG012

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
    df_location = df_extended_data['11433100_AMF']

    df_location = df_location - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SLC003']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LNG012'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1967, 1993)), 'I_LNG012')


def I_RUB002(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RUB002

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

    # these are just all zero
    df_rim_inflows['I_RUB002'] = 0

def I_NMA003(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NMA003

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
    df_location = df_extended_data['11433260']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NMA003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1966, 1986)), 'I_NMA003')


def I_MFA025(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA025

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
    df_location = df_extended_data['11433300']

    # subtract upstream
    df_location = (df_location - df_rim_inflows['I_FRMDW'] - df_rim_inflows['I_RUB002'] - df_rim_inflows['I_PLC007'] - df_rim_inflows['I_STMPY'] - df_rim_inflows['I_LNG012'] -
                   df_rim_inflows['I_SLC003'] - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SFR006'] - df_rim_inflows['I_LOONL'] - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']
                   - df_rim_inflows['I_HHOLE'] - df_rim_inflows['I_NMA003'] - df_rim_inflows['I_MFA036'] - df_rim_inflows['I_DCC010'] - df_rim_inflows['I_GERLE'])

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # watershed factor
    df_location = df_location * 0.853

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA025'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1959, 2025)), 'I_MFA025')


def I_MFA023(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA023

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
    df_location = df_rim_inflows['I_MFA025']

    # scale it based on area change
    df_location = area_scale(df_location, d_area_1=0.147, d_area_2=0.853)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA023'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1959, 2025)), 'I_MFA023')


def I_MFA001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFA001

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
    df_location = df_extended_data['11433500']

    # subtract upstream
    df_location = (df_location - df_rim_inflows['I_FRMDW'] - df_rim_inflows['I_RUB002'] - df_rim_inflows['I_PLC007'] - df_rim_inflows['I_STMPY'] - df_rim_inflows['I_LNG012'] -
                   df_rim_inflows['I_SLC003'] - df_rim_inflows['I_NLC003'] - df_rim_inflows['I_SFR006'] - df_rim_inflows['I_LOONL'] - df_rim_inflows['I_LRB004'] - df_rim_inflows['I_RUB047']
                   - df_rim_inflows['I_HHOLE'] - df_rim_inflows['I_NMA003'] - df_rim_inflows['I_MFA036'] - df_rim_inflows['I_DCC010'] - df_rim_inflows['I_GERLE'] - df_rim_inflows['I_MFA023']
                   - df_rim_inflows['I_MFA025'])

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFA001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1921, 1986)), 'I_MFA001')


def I_ALOHA(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALOHA

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
    df_location = df_extended_data['11435100_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11435100_A'].iloc[:12]

    # cale by watershed
    df_location = df_location * 0.384

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ALOHA'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(2012, 2022)), 'I_ALOHA')


def I_PYR001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_PYR001

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
    df_location = df_extended_data['11435100_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11435100_C'].iloc[:12]

    # cale by watershed
    df_location = df_location * 0.616

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_PYR001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(2012, 2022)), 'I_PYR001')


def I_CAPLS(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CAPLS

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
    df_location = df_extended_data['11437000_B']

    # first year gets the data from the A extension
    df_location.iloc[:12] = df_extended_data['11437000_A'].iloc[:12]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_CAPLS'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1993)) + list(range(1998, 2025)), 'I_CAPLS')


def I_SILVR(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SILVR

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
    df_location = df_extended_data['11436000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SILVR'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SILVR')


def I_LKVLY(df_unimpaired_data, df_full_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_LKVLY

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_nf_american = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0]

    df_nf_american.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] * 1.070, inplace=True)

    df_lake_valley_canal = df_unimpaired_data['11426190'] * df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] / (df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] +
                                                                                                                                 df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0])

    df_location = pd.Series(np.where(df_full_data['11426170'].iloc[1:] < 7.99, df_lake_valley_canal, pd.concat([df_lake_valley_canal, df_nf_american], axis=1).max(axis=1)), index=df_nf_american.index)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LKVLY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_LKVLY')


def I_NNA013(df_unimpaired_data, df_full_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_NNA013

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_nf_american = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0]

    df_nf_american.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0] * 1.070, inplace=True)

    df_lake_valley_canal = df_unimpaired_data['11426190'] * df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0] / (df_factors[df_factors['Location'] == 'I_LKVLY']['Factor'].iloc[0] +
                                                                                                                                  df_factors[df_factors['Location'] == 'I_NNA013']['Factor'].iloc[0])

    df_location = pd.Series(np.where(df_full_data['11426170'].iloc[1:] < 7.99, df_lake_valley_canal, pd.concat([df_lake_valley_canal, df_nf_american], axis=1).max(axis=1)), index=df_nf_american.index)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NNA013'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NNA013')


def I_NFA054(df_unimpaired_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA054

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_NFA054']['Factor'].iloc[0]

    df_location.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_NFA054']['Factor'].iloc[0] * 1.070, inplace=True)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA054'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA054')


def I_CYN009(df_unimpaired_data, df_rim_inflows, df_factors):
    """
    Calculate the final rim inflow for CalSim. Location: I_CYN009

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already
    df_factors: dataframe
        Watershed factors

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000'] * df_factors[df_factors['Location'] == 'I_CYN009']['Factor'].iloc[0]

    df_location.fillna(df_unimpaired_data['11426500'] * df_factors[df_factors['Location'] == 'I_CYN009']['Factor'].iloc[0] * 1.070, inplace=True)

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_CYN009'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CYN009')

def I_NFA022(df_unimpaired_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA022

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    df_location = df_unimpaired_data['11427000']

    df_location.fillna(df_unimpaired_data['11426500'] * 1.070, inplace=True)

    df_location = df_location - df_rim_inflows['I_NFA054'] - df_rim_inflows['I_NNA013'] - df_rim_inflows['I_LKVLY'] - df_rim_inflows['I_CYN009']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA022'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA022')


def I_NFA016(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFA016

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_NFA022'] * 0.070803

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFA016'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFA016')


def I_SFA076(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA076

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_SFA066'] * 0.260 / 0.443

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA076'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SFA076')


def I_SLF009(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLF009

    Parameters
    ----------
    df_unimpaired_data: dataframe
        Dataframe of unimpaired data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
        """

    df_location = df_rim_inflows['I_SFA066'] * 0.297 / 0.443

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLF009'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 2025)), 'I_SLF009')


def I_ALD004(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALD004

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
    df_location = df_extended_data['11440000_B']

    # first year uses A data
    df_location.iloc[:12] = df_extended_data['11440000_A'].iloc[:12]

    # watershed factor
    df_location = df_location * 0.848

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ALD004'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1982)), 'I_ALD004')

def I_ALD002(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ALD002

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
    df_location = df_extended_data['11440000_B']

    # first year uses A data
    df_location.iloc[:12] = df_extended_data['11440000_A'].iloc[:12]

    # watershed factor
    df_location = df_location * 0.152

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ALD002'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1982)), 'I_ALD002')


def I_PLM001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_PLM001

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
    df_location = df_extended_data['11440500_B']

    # first year uses A data
    df_location.iloc[:12] = df_extended_data['11440500_A'].iloc[:12]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_PLM001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1940)), 'I_PLM001')


def I_UNVLY(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_UNVLY

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
    df_location = df_extended_data['11441000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_UNVLY'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1925, 1961)) + [1966, 1976, 1977, 1987, 1988, 1991, 1992, 2001, 2014, 2015, 2021], 'I_UNVLY')


def I_ICEHS(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ICEHS

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
    df_location = df_extended_data['11441500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ICEHS'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1925, 2025)), 'I_ICEHS')


def I_SLV006(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLV006

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
    df_location = df_extended_data['11442000']

    # subtract upstream
    df_location = df_location - df_rim_inflows['I_UNVLY'] - df_rim_inflows['I_ICEHS']

    # redistribute negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # watershed factors
    df_location = df_location * 0.485 * 0.76

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLV006'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1962)), 'I_SLV006')


def I_SLV015(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLV006

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

    # get the already calculated location
    df_location = df_rim_inflows['I_SLV006']

    # watershed factors
    df_location = df_location * 0.584 / 0.416

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLV015'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1962)), 'I_SLV015')


def I_BSH003(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_BSH003

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

    # get the already calculated location
    df_location = df_rim_inflows['I_SLV006']

    # watershed factors
    df_location = df_location * 0.24 / 0.76

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_BSH003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1962)), 'I_BSH003')


def I_SFA040(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA040

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
    df_location = df_extended_data['11443500_D']

    df_location.loc[:datetime(1922, 9, 30)] = df_extended_data['11443500_A'].loc[:datetime(1922, 9, 30)]

    # subtract upstream
    df_location = (df_location - df_rim_inflows['I_PYR001'] - df_rim_inflows['I_ALOHA'] - df_rim_inflows['I_SFA076'] - df_rim_inflows['I_CAPLS'] - df_rim_inflows['I_SILVR']
                   - df_rim_inflows['I_SLF009'] - df_rim_inflows['I_SFA066'] - df_rim_inflows['I_ALD004'] - df_rim_inflows['I_ALD002'] - df_rim_inflows['I_PLM001']
                   - df_rim_inflows['I_UNVLY'] - df_rim_inflows['I_ICEHS'] - df_rim_inflows['I_SLV015'] - df_rim_inflows['I_SLV006'] - df_rim_inflows['I_BSH003'])

    # redistribute negatives
    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # splits which years use the redistributed negatives
    df_location.loc[:datetime(1922, 9, 30)] = df_location_positive.loc[:datetime(1922, 9, 30)]
    df_location.loc[datetime(1967,10, 31): datetime(1973, 9, 30)] = df_location_positive.loc[datetime(1967,10, 31): datetime(1973, 9, 30)]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA040'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1923, 1968)) + list(range(1974, 2025)), 'I_SFA040')


def I_RCK001(df_extended_data, df_rim_inflows):
    """
        Calculate the final rim inflow for CalSim. Location: I_RCK001

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
    df_location = df_extended_data['11444201']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_RCK001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1987, 2009)) + [2010, 2012, 2013, 2017], 'I_RCK001')


def I_SFA030(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFA030

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
    df_location = (df_extended_data['11444500'] - df_rim_inflows['I_PLM001'] - df_rim_inflows['I_ALD002'] - df_rim_inflows['I_UNVLY'] - df_rim_inflows['I_ICEHS'] - df_rim_inflows['I_SFA066']
                   - df_rim_inflows['I_CAPLS'] - df_rim_inflows['I_SILVR'] - df_rim_inflows['I_SLV015'] - df_rim_inflows['I_SLV006'] - df_rim_inflows['I_ALOHA'] - df_rim_inflows['I_PYR001']
                   - df_rim_inflows['I_BSH003'] - df_rim_inflows['I_SFA040'] - df_rim_inflows['I_RCK001'] - df_rim_inflows['I_SFA076'] - df_rim_inflows['I_SLF009'] - df_rim_inflows['I_ALD004']
                   )

    # redistribute negatives
    df_location_positive = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # the synthetic years used the redistributed negatives
    df_location.loc[:datetime(1964, 9, 30)] = df_location_positive.loc[:datetime(1964, 9, 30)]

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFA030'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1965, 2025)), 'I_SFA030')


def I_WBR001(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_WBR001

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
    df_location = df_extended_data['11446000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_WBR001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1944, 1960)), 'I_WBR001')


def I_FOLSM(df_full_data, df_unimpaired_data, df_rim_inflows):
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

    df_location = df_unimpaired_data['CalSim3'] - df_rim_inflows[['I_NNA013', 'I_NFA054','I_LKVLY', 'I_NFA022',  'I_CYN009', 'I_FRMDW','I_RUB002', 'I_STMPY', 'I_PLC007', 'I_SLC003', 'I_LNG012',
                                                            'I_NLC003',  'I_SFR006', 'I_GERLE','I_LOONL', 'I_LRB004', 'I_HHOLE', 'I_RUB047','I_NMA003', 'I_MFA036', 'I_DCC010', 'I_MFA025', 'I_MFA023',
                                                            'I_PLM001',  'I_ALD004', 'I_ALD002', 'I_UNVLY', 'I_ICEHS','I_SFA066','I_SLF009', 'I_SFA076', 'I_CAPLS', 'I_SILVR', 'I_SFA040', 'I_SFA030',
                                                            'I_MFA001', 'I_SLV015', 'I_SLV006', 'I_ALOHA', 'I_BSH003', 'I_PYR001', 'I_RCK001', 'I_WBR001', 'I_NFA016']].sum(axis=1)

    # subtract out this flow
    df_location = df_location - df_full_data['Folsom Fair Oaks']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_FOLSM'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_FOLSM')


def I_ECHOL(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ECHOL

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

    # pull out Caples
    df_location = df_rim_inflows['I_CAPLS'] * 0.385 + 0.311

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ECHOL'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, [], 'I_ECHOL')

# Upper Mokelumne rim inflows begin here

def I_SFM005(df_extended_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFM005

    Parameters
    ----------
    df_extended_data: dataframe
        Dataframe of the extended data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # pull out the relevant station
    df_location = df_extended_data['11318500']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFM005'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1934, 2025)), 'I_SFM005')


def I_MFM008(df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFM008

    Parameters
    ----------
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_full_data['11317000']

    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFM008'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1921, 2025)), 'I_MFM008')

def I_COL003(df_full_data, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_COL003

    Parameters
    ----------
    df_full_data: dataframe
        Dataframe of the gauge data to pull from
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """

    # pull out the relevant station
    df_location = df_full_data['11315000']
    # set anything negative to zero
    df_location.loc[df_location < 0] = 0

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_COL003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1921, 2025)), 'I_COL003')

def I_SLTSP(df_extended_data_bear, df_extended_data_5000, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SLTSP

    Parameters
    ----------
    df_extended_data_bear: series
        Series of the unimpaired (FNF) data from L Bear Salt Springs
    df_extended_data_5000: series
        Series of the unimpaired data from 11315000 (COL003)
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # take extended LBearSS and subtract rounded 11315000
    df_location = df_extended_data_bear - df_extended_data_5000.round(2)

    # redistribute negatives in extended LBearSS
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # multiply by (169)/(169+37.3) to match "Final Inflow" tab in sheets
    df_location = df_location * (169 / (169 + 37.3))

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SLTSP'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SLTSP')

def I_UBEAR(df_extended_data_bear, df_extended_data_5000, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_UBEAR

    Parameters
    ----------
    df_extended_data_bear: series
        Series of the extended data from Lower Bear
    df_extended_data_5000: series
        Series of the extended data from 11315000 (COL003)
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already

    Returns
    -------
    None
    """
    # take extended LBearSS and subtract rounded 11315000
    df_location = df_extended_data_bear - df_extended_data_5000.round(2)

    # redistribute negatives in extended LBearSS
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # multiply by (37.3)/(169+37.3) to match "Final Inflow" tab in sheets
    df_location = df_location * (37.3 / (169 + 37.3))

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_UBEAR'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_UBEAR')

def I_NFM010(df_11316600, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFM010

    Parameters
    ----------
    df_11316600: series
        Series of 11316600, extended with s-curve
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.

    Returns
    -------
    None
    """
    # take extended 11316600 and subtract I_UBEAR, I_SLTSP, and I_COL003
    temp1 = df_11316600
    temp2 = df_rim_inflows['I_UBEAR'].round(2)
    temp3 = df_rim_inflows['I_SLTSP'].round(2)
    temp4 = df_rim_inflows['I_COL003'].round(2)
    df_location = (df_11316600 - df_rim_inflows['I_UBEAR'].round(2)  - df_rim_inflows['I_SLTSP'].round(2)
                   - df_rim_inflows['I_COL003'].round(2))

    # redistribute negatives
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']

    # multiply by (333-21-169-37.3-7.35)/(333-21-169-37.3) to match "Final Inflow" tab in sheets
    df_location = df_location * ( 333 - 21 - 169 - 37.3 - 7.35 ) / ( 333 - 21 - 169 - 37.3 )

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero. this occurs because 1924, 1977, and 1987 had negative annual water after the
    # subtraction step a dozen lines above.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFM010'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFM010')

def I_TGC003(df_input, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_TGC003

    Parameters
    ----------
    df_input: series
        Series used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.

    Returns
    -------
    None
    """
    # take the result I_NFM010 and multiply by a watershed factor
    df_location = df_input * ( 7.35 / (333 - 7.35 - 21 - 169 - 37.3))

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_TGC003'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_TGC003')


def I_NHGAN(df_data_early, df_data_mid, df_data_late, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NHGAN

    Parameters
    ----------
    df_data_early: dataframe
        The earliest interval of data available, a one-column dataframe.
    df_data_mid: dataframe
        The middle interval of data available, a one-column dataframe.
    df_data_late: dataframe
        The latest interval of data available, a one-column dataframe.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    # this watershed factor is calculated using the total volume of precipitation on two watersheds:
    # USGS 11309500 Calaveras River at Jenny Lind and USGS 11308900 Calaveras River below New Hogan Dam
    # from 1971 to 2000. See Excel workbook CS3_I_NHGAN_Rev2022F.xlsm , sheet "Watershed" for details.
    d_watershed =  0.9412

    # multiply each dataset by the watershed factor
    df_data_early = df_data_early * d_watershed
    df_data_mid = df_data_mid * d_watershed
    df_data_late = df_data_late

    # set negative values to zero for df_data_late
    df_data_late = df_data_late.clip(lower=0)

    # df_data_mid gets an additional factor applied. Origin of factor is uncertain
    df_data_mid = df_data_mid * 1.5244

    # create two cutoff dates for filtering the data
    cutoff_1 = pd.Timestamp('1962-10-01')
    cutoff_2 = pd.Timestamp('1963-10-01')

    # we merge the three datasets, before cutoff 1 for df_data_early, between cutoff 1 and 2 for df_data_mid, and after
    # cutoff 2 for df_data_late

    df_rim_inflows['I_NHGAN'] = pd.concat([
        df_data_early[df_data_early.index < cutoff_1].iloc[:, 0],
        df_data_mid  [(df_data_mid.index >= cutoff_1) & (df_data_mid.index < cutoff_2)].iloc[:, 0],
        df_data_late [df_data_late.index >= cutoff_2].iloc[:, 0],
    ])

    df_rim_inflows['I_NHGAN'] = df_rim_inflows['I_NHGAN'].round(2)
    df_rim_inflows['I_NHGAN'] = df_rim_inflows['I_NHGAN'].clip(lower=0)

def I_PARDE(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_PARDE

    Parameters
    ----------
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    # this watershed factor is calculated using the total volume of precipitation on two watersheds:
    # "New Hogan" and "Pardee". See Excel workbook CS3_I_PARDE_Rev2022F.xlsm, sheet "Watershed" for details.
    d_watershed =  0.0700

    # multipy New Hogan by the watershed factor to create Pardee flow
    df_rim_inflows['I_PARDE'] = df_rim_inflows['I_NHGAN'] * d_watershed

    # round to 2 decimal places and set negative values to zero
    df_rim_inflows['I_PARDE'] = df_rim_inflows['I_PARDE'].round(2)
    df_rim_inflows['I_PARDE'] = df_rim_inflows['I_PARDE'].clip(lower=0)


def I_CMCHE(df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CMCHE

    Parameters
    ----------
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    # this watershed factor is calculated using the total volume of precipitation on two watersheds:
    # "New Hogan" and "Pardee". See Excel workbook CS3_I_CMCHE_Rev2022F.xlsm, sheet "Watershed" for details.
    d_watershed =  0.0700

    # multipy New Hogan by the watershed factor to create Pardee flow
    df_rim_inflows['I_CMCHE'] = df_rim_inflows['I_NHGAN'] * d_watershed

    # round to 2 decimal places and set negative values to zero
    df_rim_inflows['I_CMCHE'] = df_rim_inflows['I_CMCHE'].round(2)
    df_rim_inflows['I_CMCHE'] = df_rim_inflows['I_CMCHE'].clip(lower=0)

def I_MOK079(df_9500_FNF, df_3500, df_PARDE, df_CMCHE, df_NFM010, df_MFM008, df_UBEAR, df_SLTSP,
             df_SFM005, df_TGC003, df_COL003, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MOK079

    Parameters
    ----------
    df_9500_FNF: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_3500: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_PARDE: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_CMCHE: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_NFM010: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_MFM008: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_UBEAR: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_SLTSP: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_SFM005: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_TGC003: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_COL003: dataframe
        Single column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # Combine flows, giving an error if indices don't match
    # NOTE: the version of I_CMCHE in the MOK079 sheet doesn't match the version we have from SV INPUTS from the CMCHE
    # sheet. In our current version the SV INPUT for CMCHE is exactly the same as that for PARDE, but that's not true
    # for the I_CMCHE inside the MOK079 sheet.

    # take camanche and subtract off I_PARDE and I_CMCHE
    df_camanche_combo = (df_3500.iloc[:, 0] - df_PARDE.iloc[:, 0] - df_CMCHE.iloc[:, 0]).to_frame()

    # fill df_location with df_9500_FNF, but where df_9500_FNF is NaN, fill with df_camanche_combo
    df_location = df_9500_FNF.iloc[:, 0].fillna(df_camanche_combo.iloc[:, 0]).to_frame()

    # subtract off many SV INPUT flows
    df_location = (df_location.iloc[:, 0] - df_NFM010.iloc[:, 0] - df_MFM008.iloc[:, 0] - df_UBEAR.iloc[:, 0]
                   - df_SLTSP.iloc[:, 0] - df_SFM005.iloc[:, 0] - df_TGC003.iloc[:, 0] - df_COL003.iloc[:, 0]).to_frame()

    # round to 2 decimal places
    df_location = df_location.round(2)

    # set negative values to zero
    df_location = df_location.clip(lower=0)

    df_rim_inflows['I_MOK079'] = df_location.iloc[:, 0]

def I_JNKSN(df_11332500, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_JNKSN

    Parameters
    ----------
    df_11332500: series
        Series used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    # round to 2 decimals
    df_location = df_11332500.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_JNKSN'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_JNKSN')

def I_CMP001(df_11333000, df_jnksn, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CMP001

    Parameters
    ----------
    df_11333000: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_jnksn: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # retrieve the first column as a series. this should be the only column
    df_location = df_11333000.iloc[:, 0]

    # retrieve the first column as a series. this should be the only column
    df_jnksn_series = df_jnksn.iloc[:, 0]

    # subtract of the final flow from Jnksn and multiply by a watershed factor
    df_location = (df_location - df_jnksn_series) * (62.6 - 18.2 - 32.4) / (62.6 - 18.2)

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_CMP001'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CMP001')

def I_CMP014(df_11333000, df_jnksn, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CMP001, follows the logic of CS3_I_CMP014_Rev2022G.xlsm
    Note this is version G, not F.

    Parameters
    ----------
    df_11333000: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_jnksn: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # retrieve the first column as a series. this should be the only column
    df_location = df_11333000.iloc[:, 0]

    # retrieve the first column as a series. this should be the only column
    df_jnksn_series = df_jnksn.iloc[:, 0]

    # subtract of the final flow from Jnksn and multiply by a watershed factor
    df_location = (df_location - df_jnksn_series) * (62.6 - 18.2 - 12) / (62.6 - 18.2)

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_CMP014'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CMP014')


def I_CSM035(df_11335000, df_jnksn, df_cmp001, df_cmp014, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CSM035

    Parameters
    ----------
    df_11335000: dataframe
        One-column dataframe used as input to create the final rim inflow. Follows unimpairment in sheet CMP001.
    df_jnksn: dataframe
        The rim inflow output of I_JNKSN.
    df_cmp001: dataframe
        The rim inflow output of I_CMP001.
    df_cmp014: dataframe
        The rim inflow output of I_CMP014.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # retrieve the first column as a series. this should be the only column
    df_location = df_11335000.iloc[:, 0]

    # subtract off JNKSN, CMP001, and CMP014
    df_location = unimpaired_flows(df_location, fl_subtractions=[df_jnksn.iloc[:,0], df_cmp001.iloc[:,0],
                                                                 df_cmp014.iloc[:,0]])

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_CSM035'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CSM035')


def I_AMADR(df_11335000, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CSM035

    Parameters
    ----------
    df_11335000: dataframe
        One-column dataframe used as input to create the final rim inflow. Follows unimpairment in sheet JNKSN.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # retrieve the first column as a series. this should be the only column
    df_location = df_11335000.iloc[:, 0]

    # watershed factor calculated as the ratio of total precipitation volume ratio from 1971-2000 between
    # Cosumnes River at Michigan Bar and Jackson Creek at dam. See sheet CS3_I_AMADR_Rev2022F.xlsm, tab "Watersheds"
    d_watershed = 0.0804
    df_location = df_location * d_watershed

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_AMADR'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_AMADR')

def I_DSC035(df_11326300, df_11327000, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DSC035

    Parameters
    ----------
    df_11326300: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from DSC035 sheet.
    df_11327000: dataframe
        One-column dataframe used as input to create the final rim inflow. Model B from DSC035 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # add model A and model B
    df_location = (df_11326300.iloc[:, 0] + df_11327000.iloc[:, 0])

    # watershed factor calculated in sheet CS3_I_DSC035_Rev2022F.xlsm, tab "Watersheds"
    d_watershed = 1.335
    df_location = df_location * d_watershed

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_DSC035'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_DSC035')

def I_DEE023(df_11335700, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DEE023

    Parameters
    ----------
    df_11335700: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from DEE023 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_11335700.iloc[:, 0]

    # watershed factor calculated in sheet CS3_I_DEE023_Rev2022F.xlsm, tab "Watersheds"
    d_watershed = 1.626
    df_location = df_location * d_watershed

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_DEE023'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_DEE023')


def I_SFS033(df_11296500, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFS033

    Parameters
    ----------
    df_11296500: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from SFS033 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_11296500.iloc[:, 0].copy()

    # area factor calculated in sheet CS3_I_SFS033_Rev2022F.xlsm, tab "FINAL INFLOW"
    d_area_factor = 0.400
    df_location = df_location * d_area_factor

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFS033'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SFS033')

def I_PCRST(df_11296500, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_PCRST. This is an identical calculation to SFS033 above,
    except for a different area factor
    Parameters
    ----------
    df_11296500: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from PCRST sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_11296500.iloc[:, 0].copy()

    # area factor calculated in sheet CS3_I_PCRST_Rev2022F.xlsm, tab "FINAL INFLOW"
    d_area_factor = 0.600
    df_location = df_location * d_area_factor

    # round to 2 decimals
    df_location = df_location.round(2)

    # set anything negative to zero.
    df_location.loc[df_location < 0] = 0

    # add into the rim inflow dataframe
    df_rim_inflows['I_PCRST'] = df_location

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_PCRST')

def I_SFS030(df_location, df_I_SFS033, df_I_PCRST, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SFS030. Replicates logic from sheet CS3_I_SFS030_Rev2022F.xlsm
    Parameters
    ----------
    df_location: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from SFS030 sheet.
    df_I_SFS033: dataframe
        One-column dataframe, the rim inflow output from I_SFS033.
    df_I_PCRST: dataframe
        One-column dataframe, the rim inflow output from I_PCRST.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    # subtract the rim inflows from the other two locations
    df_location = (df_location.iloc[:,0] - df_I_SFS033.iloc[:,0] - df_I_PCRST.iloc[:,0]).to_frame(df_location.columns[0])

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # watershed (area only) factor
    df_location = df_location * 0.16

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SFS030'] = df_location

    df_location.rename(columns={'11298000': 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SFS030')


def I_LYONS(df_location, df_I_SFS033, df_I_PCRST, df_I_SFS030, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_LYONS. Replicates logic from sheet CS3_I_LYONS_Rev2022F.xlsm
    Parameters
    ----------
    df_location: dataframe
        One-column dataframe used as input to create the final rim inflow. Model A from LYONS sheet.
    df_I_SFS033: dataframe
        One-column dataframe, the rim inflow output from I_SFS033.
    df_I_PCRST: dataframe
        One-column dataframe, the rim inflow output from I_PCRST.
    df_I_SFS030: dataframe
        One-column dataframe, the rim inflow output from I_SFS030.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """
    if df_location.columns[0] == '11298000_v2':
        df_location.rename(columns={'11298000_v2': '11298000'}, inplace=True)

    # subtract the rim inflows from the other two locations
    df_location = (df_location.iloc[:,0] - df_I_SFS033.iloc[:,0] - df_I_PCRST.iloc[:,0] -
                   df_I_SFS030.iloc[:,0]).to_frame(df_location.columns[0])

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # watershed (area only) factor
    df_location = df_location * 0.84

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_LYONS'] = df_location

    df_location.rename(columns={'11298000': 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_LYONS')




def I_NFS033(df_location,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFS033. Replicates logic from sheet CS3_I_NFS033_Rev2022F.xlsm
    Parameters
    ----------
    df_location: dataframe
        One-column dataframe used as input to create the final rim inflow. Model B from NFS033 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFS033'] = df_location

    df_location.rename(columns={'11293600': 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFS033')


def I_SPICE(df_location,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_SPICE. Replicates logic from sheet CS3_I_SPICE_Rev2022G.xlsm
    Parameters
    ----------
    df_location: dataframe
        One-column dataframe used as input to create the final rim inflow. Model C from SPICE sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_SPICE'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_SPICE')


def I_BVC007(df_location,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_BVC007. Replicates logic from sheet CS3_I_BVC007_Rev2022F.xlsm
    Parameters
    ----------
    df_location: dataframe
        One-column dataframe used as input to create the final rim inflow. Model C from BVC007 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_BVC007'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_BVC007')


def I_NFS009(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFS009. Replicates logic from sheet CS3_I_NFS009_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow. Model B from NFS009 sheet.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()
    df_location = (df_location.iloc[:, 0] - df_rim_inflows['I_NFS033'] - df_rim_inflows['I_SPICE'] -
                     df_rim_inflows['I_BVC007']).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)
    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by the watershed factor
    df_location = df_location * 0.94670

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFS009'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFS009')


def I_NFS005(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_NFS005. Replicates logic from sheet CS3_I_NFS005_Rev2022F.xlsm
    The only difference between this calculation and the NFS009 calculation is the watershed factor.
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow. Model B from NFS005 sheet, identical to model
        B in NFS009.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()
    df_location = (df_location.iloc[:, 0] - df_rim_inflows['I_NFS033'] - df_rim_inflows['I_SPICE'] -
                     df_rim_inflows['I_BVC007']).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)
    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by the watershed factor
    df_location = df_location * 0.0533

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_NFS005'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_NFS005')


def I_MIL003(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MIL003. Replicates logic from sheet CS3_I_MIL003_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow. Uses the rim inflow from I_BVC007
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # multiply by what is presumably a watershed factor
    df_location = (df_location.iloc[:, 0] * (12.2/29.3)).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MIL003'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_MIL003')


def I_ANG017(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_ANG017. Replicates logic from sheet CS3_I_ANG017_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow. Uses the rim inflow from I_BVC007
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # multiply by what is presumably a watershed factor
    df_location = (df_location.iloc[:, 0] * (6/29.3)).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_ANG017'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_ANG017')


def I_RLIEF(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_RLIEF. Replicates logic from sheet CS3_I_RLIEF_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # multiply by a watershed factor
    df_location = (df_location.iloc[:, 0] * (.56)).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_RLIEF'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_RLIEF')


def I_MFS047(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFS047. Replicates logic from sheet CS3_I_MFS047_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # multiply by a watershed factor
    df_location = (df_location.iloc[:, 0] * (.44)).to_frame()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFS047'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_MFS047')


def I_CFS001(df_location_2,df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_CFS001. Replicates logic from sheet CS3_I_CFS001_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_CFS001'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_CFS001')


def I_DONLL(df_location_2, df_I_RLIEF, df_I_MFS047, df_I_CFS001, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_DONLL. Replicates logic from sheet CS3_I_DONLL_Rev2022G.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_I_RLIEF: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS047: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_CFS001: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract three other rim inflows from the location
    df_location = (df_location.iloc[:, 0] - df_I_RLIEF.iloc[:, 0] - df_I_MFS047.iloc[:, 0] -
                   df_I_CFS001.iloc[:, 0]).to_frame(df_location.columns[0])
    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by a watershed factor

    df_location = df_location * 0.78

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_DONLL'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_DONLL')


def I_MFS022(df_location_2, df_I_RLIEF, df_I_MFS047, df_I_CFS001, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFS022. Replicates logic from sheet CS3_I_MFS022_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_I_RLIEF: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS047: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_CFS001: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract three other rim inflows from the location
    df_location = (df_location.iloc[:, 0] - df_I_RLIEF.iloc[:, 0] - df_I_MFS047.iloc[:, 0] -
                   df_I_CFS001.iloc[:, 0]).to_frame(df_location.columns[0])
    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by a watershed factor

    df_location = df_location * 0.22

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFS022'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_MFS022')


def I_BEARD(df_location_2, df_I_RLIEF, df_I_MFS047, df_I_CFS001, df_I_DONLL, df_I_MFS022, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_BEARD. Replicates logic from sheet CS3_I_BEARD_Rev2022G.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_I_RLIEF: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS047: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_CFS001: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_DONLL: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS022: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract five other rim inflows from the location
    df_location = (df_location.iloc[:, 0] - df_I_RLIEF.iloc[:, 0] - df_I_MFS047.iloc[:, 0] -
                   df_I_CFS001.iloc[:, 0] - df_I_DONLL.iloc[:, 0] - df_I_MFS022.iloc[:, 0]).to_frame(df_location.columns[0])
    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by a watershed factor

    df_location = df_location * 0.76

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_BEARD'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_BEARD')


def I_MFS013(df_location_2, df_I_RLIEF, df_I_MFS047, df_I_CFS001, df_I_DONLL, df_I_MFS022, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_MFS013. Replicates logic from sheet CS3_I_MFS013_Rev2022G.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_I_RLIEF: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS047: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_CFS001: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_DONLL: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_I_MFS022: dataframe
        One-column dataframe of other rim inflow used in a subtraction step.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract five other rim inflows from the location
    df_location = (df_location.iloc[:, 0] - df_I_RLIEF.iloc[:, 0] - df_I_MFS047.iloc[:, 0] -
                   df_I_CFS001.iloc[:, 0] - df_I_DONLL.iloc[:, 0] - df_I_MFS022.iloc[:, 0]).to_frame(df_location.columns[0])
    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # redistribute any negatives
    df_location = remove_negatives_timeseries(df_location)

    # multiply by a watershed factor

    df_location = df_location * 0.24

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_MFS013'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_MFS013')


def I_TULOC(df_location_2, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_TULOC. Replicates logic from sheet CS3_I_TULOC_Rev2022F.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract five other rim inflows from the location
    df_location = (df_location.iloc[:, 0]).to_frame(df_location.columns[0])

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # multiply by a watershed factor
    df_location = df_location * 0.1503

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_TULOC'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_TULOC')


def I_STS059(df_location_2, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_STS059. Replicates logic from sheet CS3_I_STS059_Rev2022G.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # subtract five other rim inflows from the location
    df_location = (df_location.iloc[:, 0]).to_frame(df_location.columns[0])

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # multiply by a watershed factor
    df_location = df_location * 0.0318

    # round to two decimal places
    df_location = df_location.round(2)

    # set anything negative to zero
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # add into the rim inflow dataframe
    df_rim_inflows['I_STS059'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_STS059')


def I_STS072(df_location_2, df_rim_inflows):
    """
    Calculate the final rim inflow for CalSim. Location: I_STS072. Replicates logic from sheet CS3_I_STS072_Rev2022G.xlsm
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # subtract many previously calculated rim inflows
    df_location['TAF'] = df_location['TAF'] - df_rim_inflows['I_STS059']-df_rim_inflows['I_TULOC']-df_rim_inflows['I_RLIEF']- \
                  df_rim_inflows['I_MFS047']- df_rim_inflows['I_CFS001']- df_rim_inflows['I_DONLL']- df_rim_inflows['I_MFS022']- \
                  df_rim_inflows['I_NFS033']- df_rim_inflows['I_SPICE']-  df_rim_inflows['I_NFS009']-df_rim_inflows['I_BVC007']- \
                  df_rim_inflows['I_MIL003']- df_rim_inflows['I_NFS005']- df_rim_inflows['I_ANG017']-df_rim_inflows['I_MFS013']- \
                  df_rim_inflows['I_BEARD']-  df_rim_inflows['I_SFS033']- df_rim_inflows['I_LYONS']- df_rim_inflows['I_SFS030']- \
                  df_rim_inflows['I_PCRST']

    # set anything negative to zero (note, this step is on the "REDISTRIBUTION" sheet in Excel workbook)
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_STS072'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_STS072')


def I_STS072_v2(df_location_2, df_rim_inflows, df_data):
    """
    Calculate the final rim inflow for CalSim. Location: I_STS072. Replicates logic from sheet CS3_I_STS072_Rev2022G.xlsm
    This version exists to replicate the excel sheet using rim inflows from that sheet.
    Parameters
    ----------
    df_location_2: dataframe
        One-column dataframe used as input to create the final rim inflow.
    df_rim_inflows: dataframe
        Dataframe of rim inflows that have been calculated already. Also target dataframe for newly created rim inflow.
    Returns
    -------
    None
    """

    df_location = df_location_2.copy()

    # rename column
    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # subtract many previously calculated rim inflows
    df_location['TAF'] = df_location['TAF'] - df_data['I_STS059']-df_data['I_TULOC']-df_data['I_RLIEF']- \
                  df_data['I_MFS047']- df_data['I_CFS001']- df_data['I_DONLL']- df_data['I_MFS022']- \
                  df_data['I_NFS033']- df_data['I_SPICE']-  df_data['I_NFS009']-df_data['I_BVC007']- \
                  df_data['I_MIL003']- df_data['I_NFS005']- df_data['I_ANG017']-df_data['I_MFS013']- \
                  df_data['I_BEARD']-  df_data['I_SFS033']- df_data['I_LYONS']- df_data['I_SFS030']- \
                  df_data['I_PCRST']

    # set anything negative to zero (note, this step is on the "REDISTRIBUTION" sheet in Excel workbook)
    df_location[df_location.columns[0]] = df_location[df_location.columns[0]].clip(lower=0)

    # round to two decimal places
    df_location = df_location.round(2)

    # add into the rim inflow dataframe
    df_rim_inflows['I_STS072'] = df_location

    df_location.rename(columns={df_location.columns[0]: 'TAF'}, inplace=True)

    # create the plots to compare the observed vs synthetic data
    create_final_flow_plots(df_location, list(range(1922, 2025)), 'I_STS072')