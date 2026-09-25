import pandas as pd
from extension_functions import unimpaired_flows, get_diversions, sum_if_all_not_nan, s_curve_disaggregation, monthly_to_timeseries, remove_negatives_timeseries
import numpy as np
from datetime import datetime

def unimpaired_11439501(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11439501 SF AMERICAN R NR KYBURZ TOTAL FLOW CA. Follows the logic from CS3_I_SFA066_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in Caples, Silver, and Aloha storage and Caples, Silver, and Aloha evaporation, and subtracts Echo Lake Conduit flow

    # 11439501: South Fork American River near Kyburz (what we are unimpairing)
    # 11434500: Echo Lake Conduit
    # 11436950: Caples Lake
    # 11435900: Silver Lake
    # 11434900: Lake Aloha

    df_unimpaired = unimpaired_flows(df_gauge_data['11439501'],
                                     fl_storages=[df_gauge_data['11436950'].fillna(0), df_gauge_data['11435900'], df_gauge_data['11434900'].fillna(0)],
                                     fl_additions=[df_gauge_data['11436950_evap'].fillna(0), df_gauge_data['11435900_evap'], df_gauge_data['11434900_evap'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11434500']])

    return df_unimpaired


def unimpaired_11427500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427500 MF AMERICAN R A FRENCH MEADOWS CA. Follows the logic from CS3_I_FRMDW_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in French Meadows storage, French Meadows evaporation, and French Meadows power plant and subtracts Duncan Creek Diversion

    # Calculate duncan creek diversion
    df_duncan_creek_diversions = get_diversions(df_gauge_data['11427700'], df_gauge_data['11427750'], 9.94, 10.5)

    # 11427500: Middle Fork American River at French Meadows (what we are unimpairing)
    # 11427400: French Meadows Reservoir
    # 11427200: French Meadows Power Plant
    # df_duncan_creek_diversions: Duncan Creek Diversions (previously calculated)
    df_unimpaired = unimpaired_flows(df_gauge_data['11427500'],
                                     fl_storages=[df_gauge_data['11427400']],
                                     fl_additions=[df_gauge_data['11427200'], df_gauge_data['11427400_evap']],
                                     fl_subtractions=[df_duncan_creek_diversions])

    return df_unimpaired


def unimpaired_11427760(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427760 MF AMERICAN R AB MF PH NR FORESTHILL CA. Follows the logic from CS3_I_MFA036_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Add differences in French Meadows storage, French Meadows evaporation, and French Meadows power plant

    # 11427760: Middle Fork American River above North Fork near Foresthill (what we are unimpairing)
    # 11427400: French Meadows Reservoir
    # 11427200: French Meadows Power Plant
    df_unimpaired = unimpaired_flows(df_gauge_data['11427760'],
                                     fl_storages=[df_gauge_data['11427400']],
                                     fl_additions=[df_gauge_data['11427200'], df_gauge_data['11427400_evap']],
                                     )

    return df_unimpaired


def unimpaired_11428000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428000 RUBICON R A RUBICON SPRINGS NR MEEKS BAY CA. Follows the logic from CS3_I_RUB047_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Rubicon Rockbound Tunnel

    # 11428000: Rubicon River at Rubicon Springs (what we are unimpairing)
    # 11427940: Rubicon Rockbound Tunnel
    # fill na with zero because we dont want nans if that data is missing
    df_unimpaired = unimpaired_flows(df_gauge_data['11428000'],
                                     fl_additions=[df_gauge_data['11427940'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11428400(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428400 L RUBICON R BL BUCK ISLAND DAM CA. Follows the logic from CS3_I_LRB004_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Buck Loon Tunnel and subtracts Rubicon Rockbound Tunnel

    # 11428400: Little Rubicon River (what we are unimpairing)
    # 11428300: Buck Loon Tunnel
    # 11427940: Rubicon Rockbound Tunnel
    df_unimpaired = unimpaired_flows(df_gauge_data['11428400'],
                                     fl_additions=[df_gauge_data['11428300']],
                                     fl_subtractions=[df_gauge_data['11427940']],
                                     )

    return df_unimpaired


def unimpaired_11428800(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11428800 RUBICON R BL HELL HOLE DAM CA. Follows the logic from CS3_I_HHOLE_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Hell Hole storage differences, Hell Hole evaporation, Middle Fork PH, and Buck Look Tunnel, and subtracts French Meadows power plant and Long Canyon Canal diversions

    # 11428800: Rubicon River below Hell Hole (what we are unimpairing)
    # 11428700: Hell Hole Reservoir
    # 11428600: Middle Fork PH
    # 11428300: Buck Look Tunnel
    # 11427200: French Meadows power plant
    # 11433060: South Fork Long Canyon Canal diversions
    # 11433080: North Fork Long Canyon Canal Diversions
    # fill the nans with zeros for the locations where we can skip if it is a nan
    df_unimpaired = unimpaired_flows(df_gauge_data['11428800'],
                                     fl_storages=[df_gauge_data['11428700']],
                                     fl_additions=[df_gauge_data['11428700_evap'], df_gauge_data['11428600'].fillna(0), df_gauge_data['11428300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11427200'], df_gauge_data['11433060'].fillna(0), df_gauge_data['11433080'].fillna(0)],
                                     )

    return df_unimpaired


def unimpaired_11429500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11429500 GERLE C BL LOON LK NR MEEKS BAY CA. Follows the logic from CS3_I_LOONL_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Loon Lake storage differences and Loon Lake evaporation and subtracts Buck Look Tunnel

    # 11429500: Gerle Creek below Loon Lake (what we are unimpairing)
    # 11429340: Loon Lake PH
    # 11429350: Loon Lake
    # 11428300: Buck Look Tunnel

    # this will be when there is data for 11429340
    df_unimpaired_all = unimpaired_flows(df_gauge_data['11429500'],
                                     fl_storages=[df_gauge_data['11429350'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11429340'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11428300'].fillna(0)],
                                     )

    # this will be when there is no data for 11429340 but is reservoir data
    df_unimpaired_no_ph = unimpaired_flows(df_gauge_data['11429500'],
                                         fl_storages=[df_gauge_data['11429350'].fillna(0)],
                                         fl_additions=[df_gauge_data['11429350_evap'].fillna(0)],
                                         fl_subtractions=[df_gauge_data['11428300'].fillna(0)],
                                         )

    # combine these with the gauge data used when it is the only data
    df_unimpaired = np.where(~df_gauge_data['11429340'].isna(),
                             df_unimpaired_all,
                             np.where(~df_gauge_data['11429500'].isna() & ((df_gauge_data['11429350'].isna()) | (df_gauge_data['11429350'] == 0)),
                                      df_gauge_data['11429500'],
                                      df_unimpaired_no_ph))

    return df_unimpaired

def unimpaired_11430000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11430000 SF RUBICON R BL GERLE C NR GEORGETOWN CA. Follows the logic from CS3_I_SFR006_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Gerle Reservoir evap and Robbs Peak powerhouse and subtracts Gerle Creek below Loon Lake and Loon Lake powerhouse

    # 11430000: SF Rubicon River below Gerle Creek (what we are unimpairing)
    # 11429600: Gerle Reservoir
    # 11429300: Robbs Peak Powerhouse
    # 11429500: Gerle Creek below Loon Lake
    # 11429340: Loon Lake Powerhouse

    # if 11429600_evap, 11429300, or 11429340 are nans, just skip. so fill with zeros
    df_unimpaired = unimpaired_flows(df_gauge_data['11430000'],
                                     fl_additions=[df_gauge_data['11429600_evap'].fillna(0), df_gauge_data['11429300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11429500'], df_gauge_data['11429340'].fillna(0)],
                                     )


    return df_unimpaired

def unimpaired_11433040(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433040 PILOT C BL MUTTON CANYON NR GEORGETOWN CA. Follows the logic from CS3_I_STMPY_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in Stumpy Meadows storage differences, Stumpy Meadows evaporation and Georgetown divide ditch

    # 11433040: Pilot Creek below Mutton Canyon
    # EDN: Stumpy Meadows Reservoir
    # 11432000: Georgetown divide ditch

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433040'],
                                     fl_storages=[df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433100(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433100 LONG CANYON C NR FRENCH MEADOWS CA. Follows the logic from CS3_I_NCL003_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # Adds in North and South Fork Long Canyon Canal Diversions

    # 11433100: Long Canyon Creek near French Meadows
    # 11433060: South Fork Long Canyon Canal diversions
    # 11433080: North Fork Long Canyon Canal Diversions

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433100'],
                                     fl_additions=[df_gauge_data['11433060'].fillna(0), df_gauge_data['11433080'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433300(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433300 MF AMERICAN R NR FORESTHILL CA. Follows the logic from CS3_I_MFA025_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11433300: Middle Fork of the American near Foresthill (what we are unimpairing)
    # 11429350: Loon Lake
    # 11428700: Hell Hole
    # 11427400: French Meadows
    # EDN: Stumpy Meadows
    # 11432000: Georgetown divide ditch
    # 11429300: Robbs Peak powerhouse

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433300'],
                                     fl_storages=[df_gauge_data['11429350'].fillna(0), df_gauge_data['11428700'].fillna(0), df_gauge_data['11427400'].fillna(0), df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11428700_evap'].fillna(0), df_gauge_data['11427400_evap'].fillna(0),
                                                   df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'].fillna(0), df_gauge_data['11429300'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11433500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11433500 MF AMERICAN R NR AUBURN CA. Follows the logic from CS3_I_MFA001_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11433500: Middle Fork of the American near Auburn (what we are unimpairing)
    # 11429350: Loon Lake
    # 11428700: Hell Hole
    # 11427400: French Meadows
    # EDN: Stumpy Meadows
    # 11432000: Georgetown divide ditch
    # 11429300: Robbs Peak powerhouse

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11433500'],
                                     fl_storages=[df_gauge_data['11429350'].fillna(0), df_gauge_data['11428700'].fillna(0), df_gauge_data['11427400'].fillna(0), df_gauge_data['EDN'].fillna(0)],
                                     fl_additions=[df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11428700_evap'].fillna(0), df_gauge_data['11427400_evap'].fillna(0),
                                                   df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11432000'], df_gauge_data['11429300'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11435100(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11435100 PYRAMID C A TWIN BRIDGES CA. Follows the logic from CS3_I_ALOHA_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11435100: Pyramid creek (what we are unimpairing)
    # 11434900: Lake Aloha

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11435100'],
                                     fl_storages=[df_gauge_data['11434900']],
                                     fl_additions=[df_gauge_data['11434900_evap'].fillna(0)]
                                     )

    return df_unimpaired


def unimpaired_11437000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11437000 CAPLES LK OUTLET NR KIRKWOOD CA. Follows the logic from CS3_I_CAPLS_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11437000: Caples Lake outlet (what we are unimpairing)
    # 11436999: Caples release
    # 11437500: Caples Spill
    # 11436950: Caples Lake

    # first fill what is missing with release + spill
    df_gauge_data['11437000_EXT'] = df_gauge_data['11437000'].fillna(df_gauge_data['11436999'] + df_gauge_data['11437500'])

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11437000_EXT'],
                                     fl_storages=[df_gauge_data['11436950']],
                                     fl_additions=[df_gauge_data['11436950_evap']]
                                     )

    return df_unimpaired


def unimpaired_11436000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11436000 SILVER LK OUTLET NR KIRKWOOD CA. Follows the logic from CS3_I_SILVR_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11436000: Silver Lake outlet (what we are unimpairing)
    # 11435900: Silver Lake

    # calcualte seepage for different storages
    df_seepage = pd.DataFrame(np.arange(0, 10.1, 0.1), columns=['Storage'])
    df_seepage['Seepage'] = 0.02733 * (df_seepage['Storage'] ** 2) - 0.13408 * df_seepage['Storage'] + 0.01
    df_seepage.loc[df_seepage['Storage'] < 5, 'Seepage'] = 0
    df_seepage['Storage'] = df_seepage['Storage'].round(1)

    # match based on the storage
    # this will get the largest value below or equal to the storage value
    df_gauge_data['11435900_seepage'] = (np.floor(df_gauge_data[['11435900']] * 10) / 10).merge(df_seepage, how='left', left_on='11435900', right_on='Storage')['Seepage'].values

    # if any are nans, fill with zeros so they can be skipped
    df_unimpaired = unimpaired_flows(df_gauge_data['11436000'],
                                     fl_storages=[df_gauge_data['11435900'].fillna(0)],
                                     fl_additions=[df_gauge_data['11435900_evap'].fillna(0), df_gauge_data['11435900_seepage']]
                                     )

    return df_unimpaired


def unimpaired_11426190(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11426190 LAKE VALLEY CN NR EMIGRANT GAP  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11426190: Lake Valley canal (what we are unimpairing)
    # 11426170: Lake Valley
    # YB236: Fish release from lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11426190'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['YB236']]
                                     )

    return df_unimpaired


def unimpaired_11427000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11427000 NF AMERICAN R A NORTH FORK DAM  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11427000: North Fork american river at north fork dam (what we are unimpairing)
    # 11426170: Lake Valley
    # 11426190: Lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11427000'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['11426190']]
                                     )

    return df_unimpaired


def unimpaired_11426500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11426500 NF AMERICAN R NR COLFAX  CA. Follows the logic from CS3_I_LKVLY_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11426500: North Fork American river near Colfax (what we are unimpairing)
    # 11426170: Lake Valley
    # 11426190: Lake valley canal

    df_unimpaired = unimpaired_flows(df_gauge_data['11426500'],
                                     fl_storages=[df_gauge_data['11426170']],
                                     fl_additions=[df_gauge_data['11426170_evap'], df_gauge_data['11426190']]
                                     )

    return df_unimpaired


def unimpaired_11441000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11441000 SILVER C A UNION VALLEY CA. Follows the logic from CS3_I_UNVLY_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11441000: Silver Creek at Union Valley (what we are unimpairing)
    # 11441002: Union Valley powerhouse
    # 11441001: Union Valley Reservoir
    # 11440900: Jones Fork power plant
    # 11429300: Robbs Peak powerhouse

    # 11441001_spill: Union Valley Spill
    df_gauge_data['11441001_spill'] = pd.Series(np.where((df_gauge_data['11441001'] < 225) | (df_gauge_data['11441001'].isna()), 0, np.nan), index=df_gauge_data.index)

    df_unimpaired = unimpaired_flows(df_gauge_data['11441002'],
                                     fl_storages=[df_gauge_data['11441001'].fillna(0)],
                                     fl_additions=[df_gauge_data['11441001_spill'], df_gauge_data['11441001_evap'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11440900'].fillna(0), df_gauge_data['11429300'].fillna(0)],
                                     )

    # this location is the default
    df_final = df_gauge_data['11441000']

    # where it is missing, filled with the calculate unimpaired flows
    df_final.fillna(df_unimpaired, inplace=True)

    return df_final


def unimpaired_11441500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11441500 SF SILVER C NR ICE HOUSE CA. Follows the logic from CS3_I_ICEHS_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11441500: North Fork American river near Colfax (what we are unimpairing)
    # 11441100: Ice House Reservoir
    # 11440900: Jones Fork power plant, uses different data than other locations

    df_unimpaired = unimpaired_flows(df_gauge_data['11441500'],
                                     fl_storages=[df_gauge_data['11441100'].fillna(0)],
                                     fl_additions=[df_gauge_data['11440900'].fillna(0), df_gauge_data['11441100_evap'].fillna(0)],
                                     )

    return df_unimpaired


def unimpaired_11443500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11443500 SF AMERICAN R NR CAMINO CA. Follows the logic from CS3_I_SFA040_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11443500: South fork of the american near camino (what we are unimpairing)
    # 11443501: South fork of the american near camino + american river flume near camino
    # 11443460: South fork of the american
    # El Dorado: el dorado export
    # 11429300: Robbs Peak powerhouse
    # 11434500: Echo Lake Conduit
    # 11436950: Caples Lake
    # 11435900: Silver Lake
    # 11434900: Lake Aloha
    # 11441001: Union Valley Reservoir
    # 11441100: Ice House Reservoir
    # 11443450: Slab Creek Reservoir

    df_location = df_gauge_data['11443500'] + df_gauge_data['11443460'].fillna(0)
    df_location.loc[datetime(1922,10,31): datetime(1964, 11, 30)] = df_gauge_data.loc[datetime(1922,10,31): datetime(1964, 11, 30), '11443501']

    df_unimpaired = unimpaired_flows(df_location,
                                     fl_storages=[df_gauge_data['11436950'].fillna(0), df_gauge_data['11435900'].fillna(0), df_gauge_data['11434900'].fillna(0), df_gauge_data['11441001'].fillna(0),
                                                  df_gauge_data['11441100'].fillna(0), df_gauge_data['11443450'].fillna(0)],
                                     fl_additions=[df_gauge_data['11436950_evap'].fillna(0), df_gauge_data['11435900_evap'].fillna(0), df_gauge_data['11434900_evap'].fillna(0),
                                                   df_gauge_data['11441001_evap'].fillna(0), df_gauge_data['11441100_evap'].fillna(0), df_gauge_data['El Dorado'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11429300'].fillna(0), df_gauge_data['11434500'].fillna(0)]
                                     )

    df_unimpaired.loc[datetime(1921, 10, 31): datetime(1922, 9, 30)] = np.nan
    df_unimpaired.loc[datetime(1967,10, 31): datetime(1973, 9, 30)] = np.nan

    return df_unimpaired


def unimpaired_11444500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11444500 SF AMERICAN R NR PLACERVILLE CA. Follows the logic from CS3_I_SFA040_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11444500: South fork of the american (what we are unimpairing)
    # El Dorado: el dorado export
    # 11429300: Robbs Peak powerhouse
    # 11434500: Echo Lake Conduit
    # 11436950: Caples Lake
    # 11435900: Silver Lake
    # 11434900: Lake Aloha
    # 11441001: Union Valley Reservoir
    # 11441100: Ice House Reservoir
    # 11443450: Slab Creek Reservoir

    df_unimpaired = unimpaired_flows(df_gauge_data['11444500'],
                                     fl_storages=[df_gauge_data['11436950'].fillna(0), df_gauge_data['11435900'].fillna(0), df_gauge_data['11434900'].fillna(0), df_gauge_data['11441001'].fillna(0),
                                                  df_gauge_data['11441100'].fillna(0), df_gauge_data['11443450'].fillna(0)],
                                     fl_additions=[df_gauge_data['11436950_evap'].fillna(0), df_gauge_data['11435900_evap'].fillna(0), df_gauge_data['11434900_evap'].fillna(0),
                                                   df_gauge_data['11441001_evap'].fillna(0), df_gauge_data['11441100_evap'].fillna(0), df_gauge_data['El Dorado'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11429300'].fillna(0), df_gauge_data['11434500'].fillna(0)]
                                    )

    return df_unimpaired


def unimpaired_11444201(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11444201 ROCK C NR PLACERVILLE CA. Follows the logic from CS3_I_RCK001_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11444201: Rock Creek near placerville (what we are unimpairing)
    # 11444280: Rock Creek

    df_unimpaired = unimpaired_flows(df_gauge_data['11444201'],
                                     fl_additions=[df_gauge_data['11444280']]
                                     )

    return df_unimpaired


def unimpaired_calsim3(df_gauge_data):
    """
    Calculate the unimpaired flow for CALCULATED UNIMPAIRED FLOW AT FAIR OAKS. Follows the logic from CS3_I_FOLSM_Rev2022G

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11446500: Fair Oaks
    # YB90: South Canal below Wise powerhouse
    # YB91: Lower Greeley Canal
    # 11425416: Newcastle
    # 11434500: Echo Lake Conduit
    # PCWA Pump Station
    # El Dorado: el dorado export
    # 11432000: GD Ditch
    # 11426190: Lake Valley Canal
    # EID Diversions
    # Folsom Diversions
    # Folsom South Canal
    # 11426170: Lake Valley
    # 11436950: Caples Lake
    # 11435900: Silver Lake
    # 11434900: Lake Aloha
    # 11441001: Union Valley Reservoir
    # 11441100: Ice House Reservoir
    # 11443450: Slab Creek Reservoir
    # EDN: Stumpy Meadows
    # 11429350: Loon Lake
    # 11427400: French Meadows Reservoir
    # 11428700: Hell Hole Reservoir
    # Folsom: Folsom storage
    # NAT: Natoma storage

    # there is a timeseries that is max(11425416, YB90-YB91) for Dec 2017 and before and 11425416+11433930 Jan 2018 and on
    df_temporary = df_gauge_data['YB90'] - df_gauge_data['YB91']
    df_temporary = pd.concat([df_temporary, df_gauge_data['11425416']], axis=1).max(axis=1)
    df_temporary.loc[datetime(2018,1,31):] = df_gauge_data['11425416'].loc[datetime(2018,1,31):] + df_gauge_data['11433930'].loc[datetime(2018,1,31):]

    # this timeseries is just scaled
    df_gd_ditch_returns = df_gauge_data['11432000'] * 0.8 * 0.25

    df_unimpaired = unimpaired_flows(df_gauge_data['11446500'],
                                     fl_storages=[df_gauge_data['11426170'].fillna(0), df_gauge_data['11436950'].fillna(0), df_gauge_data['11435900'].fillna(0), df_gauge_data['11434900'].fillna(0),
                                                  df_gauge_data['11441001'].fillna(0), df_gauge_data['11441100'].fillna(0), df_gauge_data['11443450'].fillna(0), df_gauge_data['EDN'].fillna(0),
                                                  df_gauge_data['11429350'].fillna(0), df_gauge_data['11427400'].fillna(0), df_gauge_data['11428700'].fillna(0), df_gauge_data['Folsom'].fillna(0),
                                                  df_gauge_data['NAT'].fillna(0)],
                                     fl_additions=[df_gauge_data['11426170_evap'].fillna(0), df_gauge_data['11436950_evap'].fillna(0), df_gauge_data['11435900_evap'].fillna(0),
                                                   df_gauge_data['11434900_evap'].fillna(0), df_gauge_data['11441001_evap'].fillna(0), df_gauge_data['11441100_evap'].fillna(0),
                                                   df_gauge_data['EDN_evap'].fillna(0), df_gauge_data['11429350_evap'].fillna(0), df_gauge_data['11427400_evap'].fillna(0),
                                                   df_gauge_data['11428700_evap'].fillna(0), df_gauge_data['Folsom_evap'].fillna(0), df_gauge_data['NAT_evap'].fillna(0),
                                                   df_gauge_data['PCWA Pump Station'], df_gauge_data['El Dorado'], df_gauge_data['11432000'], df_gauge_data['11426190'],
                                                   df_gauge_data['EID Diversions'], df_gauge_data['Folsom Diversions'], df_gauge_data['Folsom South Canal']],
                                     fl_subtractions=[df_temporary, df_gauge_data['11434500'], df_gd_ditch_returns])

    return df_unimpaired

def unimpaired_11319500(df_full_gauge_data, df_extended_gauge_data):
    """
    Calculate the unimpaired flow for USGS  11319500:  MOKELUMNE R NR MOKELUMNE HILL CA.
    Follows the logic from CS3_I_COL003_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF. this is full dataset
    df_extended_gauge_data: dataframe
        Gauge data that contains any extended gauge data sets needed to unimpair the flows. in TAF.
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11319500: MOKELUMNE R NR MOKELUMNE HILL CA (what we are unimpairing)
    # 11318500: SF MOKELUMNE R NR WEST POINT CA (aka SFM005)
    # 11317000: MF MOKELUMNE R A WEST POINT CA (aka MFM008)

    # round to two decimal places
    df_11318500_rounded = df_extended_gauge_data['11318500'].round(2)
    df_11317000_rounded = df_full_gauge_data['11317000'].round(2)

    df_unimpaired = unimpaired_flows(df_full_gauge_data['11319500_v1'],
                                     fl_subtractions=[df_11318500_rounded, df_11317000_rounded]
                                     )

    return df_unimpaired

def unimpaired_lbear_salt_springs_fnf_v1(df_gauge_data, b_reproduce_error_lbear_ss):
    """
    Calculate the unimpaired flow for CALCULATED UNIMPAIRED at Lower Bear and Salt Springs. Follows the logic from
    CS3_I_SLTSP_Rev2022G.xlsm Uses LB_STORAGE_V1 to match sheet.
    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF
    b_reproduce_error_lbear_ss: boolean
        A flag to reproduce two errors in the excel sheet if true.
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11313500: SALT SPRINGS RES NR WEST POINT CA
    # 11314000: TIGER C PH COND BL SALT SPRINGS DAM CA
    # 11314500: NF MOKELUMNE R BL SALT SPRINGS DAM CA
    # 11315030: COLE C BL DIV DAM NR SALT SPRINGS DAM CA
    # 11315600: LOWER BEAR R RES NR NICHOLL CA
    # 11315900: BEAR R BL LO BEAR R DAM CA

    # there are two errors in the sheets, both in filling 11315030 with monthly averages.
    # 1) A timeshifting error in 11315030. Instead of filling NaN's with monthly averages, they are filled with the
    #    monthly average of the month 3 months prior. So a January NaN is filled with October's monthly average
    # 2) The averages have an incorrect denominator by 6. So for a monthly average that should divide by 30 months of
    #    non-NaN data, the sheet divides by 24 (for example).

    # create df_unimpaired and match row names to df_gauge_data
    df_unimpaired = pd.DataFrame(index=df_gauge_data.index)


    ### Where 11315050 is NaN, replace with monthly averages up until 'cutoff'
    # create a deep copy of 11315030 dataset
    df_11315030 = df_gauge_data[['11315030']].copy(deep=True)

    if (b_reproduce_error_lbear_ss):
        # create a copy of 11315030 timeshifted forward by 3 months to help reproduce an error in excel
        df_shifted_11315030 = df_gauge_data[['11315030']].copy(deep=True).shift(3)

    ## calculate the monthly averages of the correct 11315030 data
    # set a cutoff date so we can reproduce the monthly averages of the sheets
    s_cutoff = '2021-09-30'

    # create a cutoff copy of the data
    df_11315030_cutoff = df_11315030.loc[:s_cutoff]

    # count the number of non-NaN values per month
    df_counts_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).count()

    # sum of non‑NaN values for each month
    df_sums_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).sum()

    df_sums_by_month.columns = ['11315030']

    if (b_reproduce_error_lbear_ss):
        # this reproduces the error in CS3_I_SLTSP_Rev2022G.xlsm on sheet "Cole 11315030 in Cells W127 to AH127
        df_counts_by_month = df_counts_by_month - 6
    # find the average by diving the summed month value by the data count for that month

    # if any counts are zero meaning no data in the record for that month in any year, put NaN in df_monthly_average
    df_monthly_average = df_sums_by_month.div(df_counts_by_month.replace(0, pd.NA))

    # Build a DataFrame of monthly average values based on each row's month. df_month_map has the same row index as
    # df_shifted_11315030 and df_11315030 but with monthly averages for all months
    if (b_reproduce_error_lbear_ss):
        df_month_map = (
            df_shifted_11315030.index.to_frame(index=False)
            .set_index(df_shifted_11315030.index)
        )
    else:
        df_month_map = (
            df_11315030.index.to_frame(index=False)
            .set_index(df_11315030.index)
        )
    df_month_map['month'] = df_month_map.index.month

    df_fill_values = (
        df_month_map[['month']]
        .merge(df_monthly_average, left_on='month', right_index=True)
        .iloc[:, 1:]  # keep only the monthly-average column
    )
    if (b_reproduce_error_lbear_ss):
        df_fill_values.columns = df_shifted_11315030.columns  # match original column name
    else:
        df_fill_values.columns = df_11315030.columns  # match original column name

    # Fill NaNs
    if (b_reproduce_error_lbear_ss):
        df_filled_11315030 = df_shifted_11315030.fillna(df_fill_values)
    else:
        df_filled_11315030 = df_11315030.fillna(df_fill_values)

    df_gauge_data['11315030'] = df_filled_11315030

    # Combine flows by adding gauge data, but if any of them are NaN return Nan.
    sum_if_all_not_nan(df_unimpaired, 'LBearSS_v1', df_gauge_data, ['11315900', '11314000', '11314500',
                                                '11315030', 'SS_HIST_EVAP', 'LB_HIST_EVAP'])

    # Unimpair Little Bear Salt Springs
    df_unimpaired = unimpaired_flows(df_unimpaired['LBearSS_v1'],
                                fl_storages = [df_gauge_data['SS_STORAGE'], df_gauge_data['LB_STORAGE_V1'],
                                               df_gauge_data['PGE_OLD_RES']]
    )
    return df_unimpaired

def unimpaired_lbear_salt_springs_fnf_v2(df_gauge_data, b_reproduce_error_lbear_ss):
    """
    Calculate the unimpaired flow for CALCULATED UNIMPAIRED at Lower Bear and Salt Springs. Follows the logic from
    CS3_I_UBEAR_Rev2022G.xlsm. Uses LB_STORAGE_V2 to match sheet.
    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF
    b_reproduce_error_lbear_ss: boolean
        A flag to reproduce two errors in the excel sheet if true.
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11313500: SALT SPRINGS RES NR WEST POINT CA
    # 11314000: TIGER C PH COND BL SALT SPRINGS DAM CA
    # 11314500: NF MOKELUMNE R BL SALT SPRINGS DAM CA
    # 11315030: COLE C BL DIV DAM NR SALT SPRINGS DAM CA
    # 11315600: LOWER BEAR R RES NR NICHOLL CA
    # 11315900: BEAR R BL LO BEAR R DAM CA

    # there are two errors in the sheets, both in filling 11315030 with monthly averages.
    # 1) A timeshifting error in 11315030. Instead of filling NaN's with monthly averages, they are filled with the
    #    monthly average of the month 3 months prior. So a January NaN is filled with October's monthly average
    # 2) The averages have an incorrect denominator by 6. So for a monthly average that should divide by 30 months of
    #    non-NaN data, the sheet divides by 24 (for example).

    # create df_unimpaired and match row names to df_gauge_data
    df_unimpaired = pd.DataFrame(index=df_gauge_data.index)


    ### Where 11315050 is NaN, replace with monthly averages up until 'cutoff'
    # create a deep copy of 11315030 dataset
    df_11315030 = df_gauge_data[['11315030']].copy(deep=True)

    if (b_reproduce_error_lbear_ss):
        # create a copy of 11315030 timeshifted forward by 3 months to help reproduce an error in excel
        df_shifted_11315030 = df_gauge_data[['11315030']].copy(deep=True).shift(3)

    ## calculate the monthly averages of the correct 11315030 data
    # set a cutoff date so we can reproduce the monthly averages of the sheets
    s_cutoff = '2021-09-30'

    # create a cutoff copy of the data
    df_11315030_cutoff = df_11315030.loc[:s_cutoff]

    # count the number of non-NaN values per month
    df_counts_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).count()

    # sum of non‑NaN values for each month
    df_sums_by_month = df_11315030_cutoff.groupby(df_11315030_cutoff.index.month).sum()

    df_sums_by_month.columns = ['11315030']

    if (b_reproduce_error_lbear_ss):
        # this reproduces the error in CS3_I_SLTSP_Rev2022G.xlsm on sheet "Cole 11315030 in Cells W127 to AH127
        df_counts_by_month = df_counts_by_month - 6
    # find the average by diving the summed month value by the data count for that month

    # if any counts are zero meaning no data in the record for that month in any year, put NaN in df_monthly_average
    df_monthly_average = df_sums_by_month.div(df_counts_by_month.replace(0, pd.NA))

    # Build a DataFrame of monthly average values based on each row's month. df_month_map has the same row index as
    # df_shifted_11315030 and df_11315030 but with monthly averages for all months
    if (b_reproduce_error_lbear_ss):
        df_month_map = (
            df_shifted_11315030.index.to_frame(index=False)
            .set_index(df_shifted_11315030.index)
        )
    else:
        df_month_map = (
            df_11315030.index.to_frame(index=False)
            .set_index(df_11315030.index)
        )
    df_month_map['month'] = df_month_map.index.month

    df_fill_values = (
        df_month_map[['month']]
        .merge(df_monthly_average, left_on='month', right_index=True)
        .iloc[:, 1:]  # keep only the monthly-average column
    )
    if (b_reproduce_error_lbear_ss):
        df_fill_values.columns = df_shifted_11315030.columns  # match original column name
    else:
        df_fill_values.columns = df_11315030.columns  # match original column name

    # Fill NaNs
    if (b_reproduce_error_lbear_ss):
        df_filled_11315030 = df_shifted_11315030.fillna(df_fill_values)
    else:
        df_filled_11315030 = df_11315030.fillna(df_fill_values)

    df_gauge_data['11315030'] = df_filled_11315030

    # Combine flows by adding gauge data, but if any of them are NaN return Nan.
    sum_if_all_not_nan(df_unimpaired, 'LBearSS_v2', df_gauge_data, ['11315900', '11314000', '11314500',
                                                '11315030', 'SS_HIST_EVAP', 'LB_HIST_EVAP'])

    # Unimpair Little Bear Salt Springs
    df_unimpaired = unimpaired_flows(df_unimpaired['LBearSS_v2'],
                                fl_storages = [df_gauge_data['SS_STORAGE'], df_gauge_data['LB_STORAGE_V2'],
                                               df_gauge_data['PGE_OLD_RES']]
    )
    return df_unimpaired

def unimpaired_11316600(df_full_gauge_data, df_extended_gauge_data, df_unimpaired_data):
    """
    Calculate the unimpaired flow for USGS  11316600: NF MOKELUMNE R AB TIGER CREEK CA
    Follows the logic from CS3_I_NFM010_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
    df_extended_gauge_data: dataframe
        Gauge data that contains any extended gauge data sets needed to unimpair the flows. In TAF.
    df_unimpaired_data: dataframe
        Unimpaired gauge data from other sites used to unimpair this flow. In TAF.
    Returns
    -------
    df_temporary: dataframe
        Unpaired flow for current station
    """

    # 11313500: SALT SPRINGS RES NR WEST POINT CA
    # 11315600: LOWER BEAR R RES NR NICHOLL CA
    # 11316600: NF MOKELUMNE R AB TIGER CREEK CA
    # 11316605: TIGER CREEK BW REGULATOR RESERVOIR NR PIONEER CA
    # 11316610: TIGER CREEK POWERHOUSE NR WEST POINT CA
    # 11319500: MOKELUMNE R NR MOKELUMNE HILL CA, using this from the df_unimpaired_data, so already subtracted
    #                   I_SFM005 and I_MFM008

    # set a cutoff date for the montly averages so we get better agreement with the excel sheet
    s_cutoff = "2021-09-30"

    # create monthly average list for 11316605
    dl_monthly_avg_11316605 = (
        df_full_gauge_data.loc[:s_cutoff]  # keep rows ≤ 2021-09-30
        .groupby(df_full_gauge_data.loc[:s_cutoff].index.month)["11316605"]
        .mean()
        .tolist()
    )

    # fill list into dataframe so each month in index is filled with the correct monthly average
    df_monthly_avg_11316605 = (
        df_full_gauge_data.index.to_series().dt.month
        .map(lambda m: dl_monthly_avg_11316605[m - 1])
    )

    #copy our source data that we're unimpairing (df_full_gauge_data['11316600']) into a new dataframe with column
    # called 'TAF'

    df_temporary = unimpaired_flows(df_full_gauge_data['11316600'],
                                     fl_storages=[df_full_gauge_data['SS_STORAGE'].fillna(0),
                                                  df_full_gauge_data['LB_STORAGE_V1'].fillna(0),
                                                  df_full_gauge_data['PGE_OLD_RES'].fillna(0),],
                                     fl_additions=[df_full_gauge_data['11316610'],
                                                   df_monthly_avg_11316605,
                                                   df_full_gauge_data['LB_HIST_EVAP'].fillna(0),
                                                   df_full_gauge_data['SS_HIST_EVAP'].fillna(0),]
                                     )
    # take the lesser value of 1) unimpaired 6600 and 2) unimpaired 11319500_v1 and put it in df_temporary
    df_temporary = np.minimum(df_unimpaired_data["11319500_v1"], df_temporary)

    return df_temporary

def unimpaired_tiger_creek_conduit_accretions(df_full_gauge_data, df_extended_data):
    """
    Calculate the unimpaired flow for Tiger Creek Conduit Accretions (no USGS gage):
    Follows the logic from CS3_I_TGC003_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
    df_extended_gauge_data: dataframe
        Gauge data that contains any extended gauge data sets needed to unimpair the flows. In TAF.
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11314000: Tiger Creek Conduit, TIGER C PH COND BL SALT SPRINGS DAM CA
    # 11316605: TIGER CREEK BW REGULATOR RESERVOIR NR PIONEER CA
    # 11316610:  TIGER CREEK POWERHOUSE NR WEST POINT CA

    df_unimpaired = unimpaired_flows(df_full_gauge_data['11316610'],
                                     fl_additions=[df_full_gauge_data['11316605']],
                                     fl_subtractions=[df_full_gauge_data['11314000']]
                                     )
    # To match sheets, if any df_unimpaired values are below -999, replace with -999. This does not clip any values.
    # Count values below -999
    n_clipped = int((df_unimpaired < -999).sum())
    # Clip the series
    df_unimpaired = df_unimpaired.clip(lower=-999)

    return df_unimpaired

def unimpaired_11309500_for_NHGAN(df_full_gauge_data):
    """
    Calculate the unimpaired flow for the Calaveras River at 11309500:
    Follows the logic from CS3_I_NHGAN_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
      Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11309500: CALAVERAS R A JENNY LIND CA
    # OHGAN_STORAGE: OLD HOGAN END OF MONTH STORAGE
    # NHGAN_STORAGE: NEW HOGAN DAM END OF MONTH STORAGE
    # OHGAN_evap: Old Hogan reservoir evaporation
    # NHGAN_evap: New Hogan reservoir evaporation

    # fill in zeros in place of the negative values for both storages and both evap series

    df_ohgan_storage = df_full_gauge_data['OHGAN_STORAGE'].clip(lower=0)
    df_nhgan_storage = df_full_gauge_data['NHGAN_STORAGE'].clip(lower=0)
    df_ohgan_evap = df_full_gauge_data['OHGAN_evap'].clip(lower=0)
    df_nhgan_evap = df_full_gauge_data['NHGAN_evap'].clip(lower=0)

    #fill NaN values with zeros for evap and storage
    df_ohgan_storage.fillna(0, inplace=True)
    df_nhgan_storage.fillna(0, inplace=True)
    df_ohgan_evap.fillna(0, inplace=True)
    df_nhgan_evap.fillna(0, inplace=True)

    df_unimpaired = unimpaired_flows(df_full_gauge_data['11309500'],
                                     fl_additions=[df_ohgan_evap, df_nhgan_evap],
                                     fl_storages=[df_ohgan_storage, df_nhgan_storage]
                                     )

    return df_unimpaired

def unimpaired_NF_SF_ITAS(df_full_gauge_data):
    """
    Combines three gage data sets into one:
    Follows the logic from CS3_I_NHGAN_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
      Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11308000: NF CALAVERAS R NR SAN ANDREAS CA
    # 11306000: SF CALAVERAS R NR SAN ANDREAS CA
    # 11306500: CALAVERITAS C NR SAN ANDREAS CA

    # note: we're not really unimpairing any of these gauges, we're just adding all three

    df_unimpaired = unimpaired_flows(df_full_gauge_data['11308000'],
                                     fl_additions=[df_full_gauge_data['11306000'],
                                                   df_full_gauge_data['11306500']]
                                     )

    return df_unimpaired

def unimpaired_NH_DAM_RELEASE(df_full_gauge_data):
    """
    Calculate the unimpaired flow from New Hogan Dam Release (USACE) (no USGS gage):
    Follows the logic from CS3_I_NHGAN_Rev2022G.xlsm

    Parameters
    ----------
    df_full_gauge_data: dataframe
      Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # USACE_NH_RELEASE: USACE NEW HOGAN RESERVOIR RELEASE
    # OHGAN_STORAGE: OLD HOGAN END OF MONTH STORAGE
    # NHGAN_STORAGE: NEW HOGAN DAM END OF MONTH STORAGE
    # OHGAN_evap: Old Hogan reservoir evaporation
    # NHGAN_evap: New Hogan reservoir evaporation

    # fill in zeros in place of the negative values for storages, evaps, and the series we're unimpairing

    df_ohgan_storage = df_full_gauge_data['OHGAN_STORAGE'].clip(lower=0)
    df_nhgan_storage = df_full_gauge_data['NHGAN_STORAGE'].clip(lower=0)
    df_ohgan_evap = df_full_gauge_data['OHGAN_evap'].clip(lower=0)
    df_nhgan_evap = df_full_gauge_data['NHGAN_evap'].clip(lower=0)
    df_nh_release = df_full_gauge_data['USACE_NH_RELEASE'].clip(lower=0)

    #fill NaN values with zeros for evap and storage
    df_ohgan_storage.fillna(0, inplace=True)
    df_nhgan_storage.fillna(0, inplace=True)
    df_ohgan_evap.fillna(0, inplace=True)
    df_nhgan_evap.fillna(0, inplace=True)

    df_unimpaired = unimpaired_flows(df_nh_release,
                                     fl_additions=[df_ohgan_evap, df_nhgan_evap],
                                     fl_storages=[df_ohgan_storage, df_nhgan_storage]
                                     )

    return df_unimpaired

def unimpaired_11319500_v2(df_full_gauge_data):
    """
      Calculate the unimpaired flow from of USGS gage 11319500, stored at 11319500_v2. Not the COL003 version of
      11319500, which is stored as 11319500_v1.
      Follows the logic from CS3_I_MOK079_Rev2022G.xlsm

      Parameters
      ----------
      df_full_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
      Returns
      -------
      df_unimpaired: dataframe
          Unpaired flow for current station
      """

    # set negative values to zero for the following dataframes
    df_no_neg_salt_storage = df_full_gauge_data[['SS_STORAGE']].clip(lower=0).copy(deep=True)
    df_no_neg_lbear_storage = df_full_gauge_data[['LB_STORAGE_V1']].clip(lower=0).copy(deep=True)
    df_no_neg_pge_storage = df_full_gauge_data[['PGE_OLD_RES']].clip(lower=0).copy(deep=True)
    df_no_neg_lb_hist_evap = df_full_gauge_data[['LB_HIST_EVAP']].clip(lower=0).copy(deep=True)
    df_no_neg_ss_hist_evap = df_full_gauge_data[['SS_HIST_EVAP']].clip(lower=0).copy(deep=True)
    df_no_neg_riv_div = df_full_gauge_data[['MOK_RIV_DIV']].clip(lower=0).copy(deep=True)

    # rename the columns 'TAF' to prepare for inputting to unimpaired_flows
    df_no_neg_salt_storage.rename(columns={df_no_neg_salt_storage.columns[0]: 'TAF'}, inplace=True)
    df_no_neg_lbear_storage.rename(columns={df_no_neg_lbear_storage.columns[0]: 'TAF'}, inplace=True)
    df_no_neg_pge_storage.rename(columns={df_no_neg_pge_storage.columns[0]: 'TAF'}, inplace=True)
    df_no_neg_lb_hist_evap.rename(columns={df_no_neg_lb_hist_evap.columns[0]: 'TAF'}, inplace=True)
    df_no_neg_ss_hist_evap.rename(columns={df_no_neg_ss_hist_evap.columns[0]: 'TAF'}, inplace=True)
    df_no_neg_riv_div.rename(columns={df_no_neg_riv_div.columns[0]: 'TAF'}, inplace=True)

    #  use those values to unimpaire the 11319500_v2 data
    df_unimpaired = unimpaired_flows(df_full_gauge_data['11319500_v2'],
                                     fl_additions=[df_no_neg_lb_hist_evap, df_no_neg_ss_hist_evap,
                                                   df_no_neg_riv_div],
                                     fl_storages=[df_no_neg_salt_storage, df_no_neg_lbear_storage,
                                                  df_no_neg_pge_storage]
                                     )

    return df_unimpaired

def unimpaired_11335000(df_full_gauge_data, b_v1=True):
    """
     Calculate the unimpaired flow from of USGS gage 11335000.
     Follows the logic from CS3_I_CMP001_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """

    df_11335000 = df_full_gauge_data['11335000'].copy()
    df_export = df_full_gauge_data['CMP001_EXPORT']
    # fill in zeros in place of the negative values for storages, evaps
    df_JNKSN_evap = df_full_gauge_data['JNKSN_evap'].clip(lower=0)
    df_JNKSN_storage = df_full_gauge_data['JNKSN_STORAGE'].clip(lower=0)

    if not b_v1:
        #for version 2, we use zero for the storage in december of 1965
        df_JNKSN_storage.loc['1965-12-31'] = 0
    # fill NaN values with zeros for evap and storage
    df_11335000.fillna(0, inplace=True)
    df_export.fillna(0, inplace=True)
    df_JNKSN_evap.fillna(0, inplace=True)
    df_JNKSN_storage.fillna(0, inplace=True)

    # combine storage diff, evap, and export
    df_unimpaired_temp = unimpaired_flows(df_export, fl_additions=[df_JNKSN_evap], fl_storages=[df_JNKSN_storage])
    # clip negatives to zero
    df_unimpaired_temp = df_unimpaired_temp.clip(lower=0)

    df_unimpaired = unimpaired_flows(df_11335000, fl_additions=[df_unimpaired_temp])

    return df_unimpaired


def unimpaired_11333000(df_full_gauge_data):
    """
     Calculate the unimpaired flow from of USGS gage 11333000.
     Follows the logic from CS3_I_CMP001_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """

    df_11333000 = df_full_gauge_data['11333000'].copy()
    df_export = df_full_gauge_data['CMP001_EXPORT']
    # fill in zeros in place of the negative values for storages, evaps, and export diversion
    df_JNKSN_evap = df_full_gauge_data['JNKSN_evap'].clip(lower=0)
    df_JNKSN_storage = df_full_gauge_data['JNKSN_STORAGE'].clip(lower=0)
    df_export = df_export.clip(lower=0)

    # fill NaN values with zeros for evap and storage
    df_export.fillna(0, inplace=True)
    df_JNKSN_evap.fillna(0, inplace=True)
    df_JNKSN_storage.fillna(0, inplace=True)

    # combine storage diff, evap, and export
    df_unimpaired = unimpaired_flows(df_11333000, fl_additions=[df_JNKSN_evap, df_export],
                                          fl_storages=[df_JNKSN_storage])

    return df_unimpaired


def unimpaired_11409000(df_full_gauge_data):
    """
     Calculate the unimpaired flow for USGS 11409000 M YUBA R AB OREGON C NR NORTH SAN JUAN CA
.
     Follows the logic from CS3_I_NFY029_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """

    df_11409000 = df_full_gauge_data.loc[:, "11409000"].fillna(
        df_full_gauge_data.loc[:, "11410000"] - df_full_gauge_data.loc[:, "11409500"]
    )

    # only until 1968
    df_storage = df_full_gauge_data.loc[:, "11407800_I_NFY029"]
    
    df_unimpaired = unimpaired_flows(
        df_11409000,
        fl_additions=[
            df_full_gauge_data.loc[:, "JKSMD_evap_I_NFY029"].fillna(0),
            df_full_gauge_data.loc[:, "11408000"].fillna(0)
        ],
        # Gaurav: we should not fill storage with 0, we should do df_storage.diff().fillna(0)
        fl_storages = [df_storage.fillna(0)]
        )
    return df_unimpaired


def unimpaired_11416500(df_full_gauge_data, df_extended_data):
    """
     Calculate the unimpaired flow for USGS 11416500 CANYON C BL BOWMAN LK CA
     Follows the logic from CS3_I_BOWMN_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     df_extended_data: dataframe
       Dataframe of the extended data to pull from
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """

    df_11416500 = df_full_gauge_data.loc[:, "11416500"]

    stor_Bowman = df_full_gauge_data.loc[:, "11415500"]
    stor_French = df_full_gauge_data.loc[:, "11414400_I_BOWMN"]
    stor_Faucherie = df_full_gauge_data.loc[:, "11414440_I_BOWMN"]
    stor_Sawmill = df_full_gauge_data.loc[:, "11414465_I_BOWMN"]
    
    evap_Bowman = df_full_gauge_data.loc[:, 'BOWMN_evap']
    evap_French = df_full_gauge_data.loc[:, 'FRNCH_evap']

    df_modelB = df_extended_data.loc[:, "WILSON_CREEK"]
    df_unimpaired = unimpaired_flows(
        df_11416500,
        fl_additions=[
            df_full_gauge_data.loc[:, "11416000"].clip(lower=0).fillna(0),
            evap_Bowman.fillna(0),
            evap_French.fillna(0),
        ],
        fl_subtractions = [
            (df_full_gauge_data.loc[:, "11408000"] - df_modelB).clip(lower=0).fillna(0)
        ],
        # Gaurav: we should not fill storage with 0, we should do df_storage.diff().fillna(0)
        fl_storages = [
            stor_Bowman.fillna(0),
            stor_French.fillna(0),
            stor_Faucherie.fillna(0),
            stor_Sawmill.fillna(0)
        ]
        )
    return df_unimpaired


def unimpaired_11407900(df_full_gauge_data, df_unimpaired_data):
    """
     Calculate the unimpaired flow for USGS 11407900 M YUBA R BL JACKSON MDWS DAM NR SIERRA CITY CA.
     Follows the logic from CS3_I_JKSMD_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     df_unimpaired_data: dataframe
       unimpaired data for all nodes before this as this node depends on one
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_unimp_11407900 = unimpaired_flows(
        df_full_gauge_data.loc[:, "11407900"],
        fl_additions=[
            df_full_gauge_data.loc[:, "JKSMD_evap"].clip(lower=0).fillna(0)
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "11407800"].clip(lower=0).fillna(0)
        ],
    )
    df_unimpaired_filled = (df_unimpaired_data["11408550"] * 38.3 / 39.8).fillna(df_unimp_11407900)
    return df_unimpaired_filled


def unimpaired_11408550(df_full_gauge_data, df_extended_data):
    """
     Calculate the unimpaired flow for USGS 11408550 M YUBA R BL MILTON DAM CA
     Follows the logic from CS3_I_JKSMD_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_unimp_11408550 = unimpaired_flows(
        pd.DataFrame({
                "a": df_full_gauge_data.loc[:, "11408550"],
                "b": df_full_gauge_data.loc[:, "11408500"]
            }).max(axis=1, skipna=True),
        fl_additions=[
            df_full_gauge_data.loc[:, "JKSMD_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "11408000"],
        ],
        fl_subtractions=[
            df_extended_data.loc[:, "WILSON_CREEK"]
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "11407800"].clip(lower=0).fillna(0)
        ],
    )
    return df_unimp_11408550


def unimpaired_11409400(df_full_gauge_data):
    """
     Calculate the unimpaired flow for USGS 11409400 OREGON C BL LOG CABIN DAM NR CAMPTONVILLE CA
     Follows the logic from CS3_I_OGN005_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_unimp_11409400 = unimpaired_flows(
        df_full_gauge_data.loc[:, "11409400"],
        fl_additions=[
            df_full_gauge_data.loc[:, "11409350"].clip(lower=0).fillna(0)
        ],
        fl_subtractions = [
            df_full_gauge_data.loc[:, "11408870"].clip(lower=0).fillna(0)
        ],
    )
    return df_unimp_11409400


def unimpaired_11409400_ext(df_full_gauge_data, df_extended_data, df_unimpaired_data):
    """
     Calculate the extended unimpaired flow for USGS 11409400 OREGON C BL LOG CABIN DAM NR CAMPTONVILLE CA
     Follows the logic from CS3_I_OGN005_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     df_extended_data: dataframe
       Dataframe of the extended data to pull from
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_unimp_11409400_ex = df_unimpaired_data["11409400"].copy(deep=True)
    ii_water_yr = df_full_gauge_data.index.map(lambda i: i.year + int(i.month>9))
    # TODO: copied this from excel, might have to calculate it?
    dl_corr_values = (
        0.830444791508848 * df_full_gauge_data.loc[:, "11409500"].groupby(ii_water_yr).sum()
        - 1.15959919555159
    )
    df_water_yr_ratios = dl_corr_values / df_full_gauge_data.loc[:, "11409500"].groupby(ii_water_yr).sum()
    df_unimp_ex = df_full_gauge_data.loc[:, "11409500"] * ii_water_yr.map(df_water_yr_ratios)
    df_unimp_11409400_ex.loc[:"1968-09"] = df_unimp_ex.loc[:"1968-09"]
    df_unimp_11409400_ex.loc["1995-10":"1996-09"] = df_extended_data.loc["1995-10":"1996-09", "11409400"]
    return df_unimp_11409400_ex


def unimpaired_11422500(df_full_gauge_data):
    """
     Calculate the unimpaired flow for USGS 11422500 BEAR R BL ROLLINS DAM NR COLFAX CA
     Follows the logic from CS3_I_RLLNS_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_unimp_11422500 = unimpaired_flows(
        df_full_gauge_data.loc[:, "11422500"],
        fl_additions=[
            df_full_gauge_data.loc[:, 'RLLNS_evap'].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "11422000"],
            df_full_gauge_data.loc[:, "YB-184"].fillna(
                pd.DataFrame({
                    "a": df_full_gauge_data.loc[:, "11421725"],
                    "b": df_full_gauge_data.loc[:, "TOWLE_CANAL"] + df_full_gauge_data.loc[:, "11421720"]
                }).max(axis=1)
            )
        ],
        fl_subtractions = [
            (
                df_full_gauge_data.loc[:, "11414200"]
                -  df_full_gauge_data.loc[:, "11414205_I_RLLNS"] / (1 - 0.125)
            ).clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "11414170"] * (1 - 0.078),
            df_full_gauge_data.loc[:, "11426190"]
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "11421800_I_RLLNS"].fillna(0)
        ]
    )
    return df_unimp_11422500


def unimpaired_11414100(df_full_gauge_data):
    """
     Calculate the unimpaired flow for USGS 11414100 FORDYCE C BL FORDYCE DAM NR CISCO CA
     Follows the logic from CS3_I_FRDYC_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    return unimpaired_flows(
        df_full_gauge_data["11414100"].clip(lower=0),
        fl_additions = [df_full_gauge_data["FRDYC_evap"]],
        fl_storages = [df_full_gauge_data["11414090"]]
    )


def unimpaired_11408880(df_full_gauge_data, df_extended_data):
    """
     Calculate the unimpaired flow for USGS 11408880 M YUBA R BL OUR HOUSE DAM CA
     Follows the logic from CS3_I_MFY013_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    return unimpaired_flows(
        df_full_gauge_data["11408880"],
        fl_additions = [
            df_full_gauge_data["11408870"].clip(lower=0).fillna(0),
            df_full_gauge_data["JKSMD_evap_I_NFY029"].clip(lower=0).fillna(0),
            (
                df_full_gauge_data["11408000"]
                - df_extended_data["WILSON_CREEK"]
            ).clip(lower=0).fillna(0)
        ],
        fl_storages = [df_full_gauge_data["11407800_I_NFY029"].fillna(0)]
    )


def unimpaired_11409000_I_MFY013(df_full_gauge_data, df_extended_data):
    """
     Calculate the unimpaired flow using I_MFY013 sheet for USGS 11409000 M YUBA R AB OREGON C NR NORTH SAN JUAN CA
     Follows the logic from CS3_I_MFY013_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    ext_11409000 = df_full_gauge_data["11409000"].fillna(
        df_full_gauge_data["11410000"] - df_full_gauge_data["11409500"]
    )
    return unimpaired_flows(
        ext_11409000,
        fl_additions = [
            df_full_gauge_data["11408870"].clip(lower=0).fillna(0),
            df_full_gauge_data["JKSMD_evap_I_NFY029"].clip(lower=0).fillna(0),
            (
                df_full_gauge_data["11408000"]
                - df_extended_data["WILSON_CREEK"]
            ).clip(lower=0).fillna(0)
        ],
        fl_storages = [df_full_gauge_data["11407800_I_NFY029"].fillna(0)]
    )


def unimpaired_11424000(df_full_gauge_data):
    """
     Calculate the unimpaired flow for USGS 11424000 BEAR R NR WHEATLAND CA
     Follows the logic from CS3_I_SFY048_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_DS_CanalSpills = df_full_gauge_data.loc[:, "DS_CANAL_SPILLS_I_RLLNS"].clip(lower=0).fillna(0)
    df_DS_CanalSpills.loc[:"2004-03"] = df_full_gauge_data.loc[:"2004-03", "DC-145"].clip(lower=0).fillna(0) * 0.6
    df_unimp_11424000 = unimpaired_flows(
        pd.DataFrame({
            "a": df_full_gauge_data.loc[:, "11424000"],
            "b": df_full_gauge_data.loc[:, "11423500"] * 1.05 - df_full_gauge_data.loc[:, "CFWID_DIVERSIONS"]
        }).max(axis=1),
        fl_additions=[
            df_full_gauge_data.loc[:, "CMPFW_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "CMBIE_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "RLLNS_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "NID_COMBIE_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "CFWID_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "SSWD_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "TARR_DITCH"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "11422000"],
            df_full_gauge_data.loc[:, "YB-184"].fillna(
                pd.DataFrame({
                    "a": df_full_gauge_data.loc[:, "11421725"],
                    "b": df_full_gauge_data.loc[:, "TOWLE_CANAL"] + df_full_gauge_data.loc[:, "11421720"]
                }).max(axis=1)
            )
        ],
        fl_subtractions = [
            df_DS_CanalSpills,
            ((
                df_full_gauge_data.loc[:, "DC-145"] - df_DS_CanalSpills
            ).clip(lower=0).fillna(0) + df_full_gauge_data.loc[:, "DC-102"])*0.2*0.85,
            (
                df_full_gauge_data.loc[:, "11414200"]
                -  df_full_gauge_data.loc[:, "11414205_I_RLLNS"] / (1 - 0.125)
            ).clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "11414170"] * (1 - 0.078),
            df_full_gauge_data.loc[:, "11426190"]
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "LAKE_COMBIE_I_RLLNS"].fillna(0),
            df_full_gauge_data.loc[:, "CAMP_FAR_I_RLLNS"].fillna(0),
            df_full_gauge_data.loc[:, "11421800_I_RLLNS"].fillna(0)
        ]
    )
    return df_unimp_11424000


def unimpaired_11424000_ACC(df_full_gauge_data, df_rim_inflows):
    """
     Calculate the unimpaired flow (accretion) for USGS 11424000 BEAR R NR WHEATLAND CA
     Follows the logic from CS3_I_CMBIE_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    df_DS_CanalSpills = df_full_gauge_data.loc[:, "DS_CANAL_SPILLS_I_RLLNS"].clip(lower=0).fillna(0)
    df_DS_CanalSpills.loc[:"2004-03"] = df_full_gauge_data.loc[:"2004-03", "DC-145"].clip(lower=0).fillna(0) * 0.6
    df_rllns = df_rim_inflows.loc[:, "I_RLLNS"]
    df_ext_BearBwRollins = df_full_gauge_data.loc[:, "11422500"].fillna(unimpaired_flows(
        df_rllns,
        fl_additions =[
            df_full_gauge_data.loc[:, "11426190"],
            df_full_gauge_data.loc[:, "11414170"] * (1 - 0.078),
            (
                df_full_gauge_data.loc[:, "11414200"]
                -  df_full_gauge_data.loc[:, "11414205_I_CMBIE"] / (1 - 0.125)
            ).clip(lower=0).fillna(0),
        ],
        fl_subtractions =[
            df_full_gauge_data.loc[:, "11422000"],
            df_full_gauge_data.loc[:, "YB-184"].fillna(
            pd.DataFrame({
                "a": df_full_gauge_data.loc[:, "11421725"],
                "b": df_full_gauge_data.loc[:, "TOWLE_CANAL"] + df_full_gauge_data.loc[:, "11421720"]
            }).max(axis=1)
            ),
            df_full_gauge_data.loc[:, "RLLNS_evap"].clip(lower=0).fillna(0),
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "11421800"].fillna(0),
        ]
    ))
    df_accretion_11424000 = unimpaired_flows(
        pd.DataFrame({
        "a": df_full_gauge_data.loc[:, "11424000"],
        "b": df_full_gauge_data.loc[:, "11423500"] * 1.05 - df_full_gauge_data.loc[:, "CFWID_DIVERSIONS"]
    }).max(axis=1) - df_ext_BearBwRollins,
        # TODO: df_ext_BearBwRollins has negative values and
        # unimpaired_flows function removes that, which messes up the
        # reproduction (moving it here now instead of fl_subtractions,
        # not sure if -ve is valid)
        fl_additions=[
            df_full_gauge_data.loc[:, "CMPFW_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "CMBIE_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "NID_COMBIE_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "CFWID_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "SSWD_DIVERSIONS"].clip(lower=0).fillna(0),
            df_full_gauge_data.loc[:, "TARR_DITCH"].clip(lower=0).fillna(0),
        ],
        fl_subtractions = [
            df_DS_CanalSpills,
            # df_ext_BearBwRollins # see note above
            ((
                df_full_gauge_data.loc[:, "DC-145"] - df_DS_CanalSpills
            ).clip(lower=0).fillna(0) + df_full_gauge_data.loc[:, "DC-102"])*0.2*0.85
        ],
        fl_storages = [
            df_full_gauge_data.loc[:, "LAKE_COMBIE"].fillna(0),
            df_full_gauge_data.loc[:, "CAMP_FAR"].fillna(0),
        ]
    )
    return df_accretion_11424000



def unimpaired_MERLC(df_full_gauge_data):
    """
     Calculate the unimpaired flow for MCollins Lake
     Follows the logic from CS3_I_MERLC_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    # get the storage for Lake Merle
    df_stor_MCollins = df_full_gauge_data.loc[:, "LAKE_MERLE"]
    df_release_MCollins = df_full_gauge_data["MERLC_RELEASE"]
    df_evap_MCollins = df_full_gauge_data["MERLC_evap"]
    df_spill_MCollins = (
        df_full_gauge_data["11420700"].clip(lower=0)
        - df_release_MCollins
        - df_full_gauge_data["DRY_CREEK_DIV_I_MERLC"]
    ).clip(lower=0) * 71.6 / 87.1
    df_spill_MCollins.loc[
        (
            ((df_stor_MCollins + df_stor_MCollins.shift(1)) / 2) < 55
        )
        & df_spill_MCollins.notna()
    ] = 0
    df_unimp_MCollins = (
        df_release_MCollins
        + df_spill_MCollins
        + df_stor_MCollins
        - df_stor_MCollins.shift(1).clip(lower=0).fillna(0)
        + df_evap_MCollins.clip(lower=0).fillna(0)
    )
    return df_unimp_MCollins


def unimpaired_11414250(df_full_gauge_data):
    """
     Calculate the unimpaired flow using I_SPLDG sheet for 11414250 S YUBA R A LANGS CROSSING NR EMIGRANT GAP CA
     Follows the logic from CS3_I_SPLDG_Rev2022G.xlsm

     Parameters
     ----------
     df_full_gauge_data: dataframe
       Gauge data that contains the current station and all needed to unimpair the flows. In TAF. This is full dataset
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    return unimpaired_flows(
        df_full_gauge_data["11414250"].clip(lower=0),
        fl_additions = [
            df_full_gauge_data["11414170"].clip(lower=0),
            df_full_gauge_data["11414200"].clip(lower=0),
            df_full_gauge_data["SPLDG_evap"].clip(lower=0).fillna(0),
            df_full_gauge_data["FRDYC_evap"].clip(lower=0).fillna(0),
        ],
        fl_storages = [
            df_full_gauge_data["11414140"].fillna(0),
            df_full_gauge_data["11414090"].fillna(0)
        ],
        fl_subtractions = [
            pd.DataFrame({
                "a":df_full_gauge_data["11416100"],
                "b":df_full_gauge_data["11416200"]
            }).max(axis=1)
        ]
    )


def unimpaired_FERC():
    """
     Calculate the unimpaired flow using I_LCBRF sheet for Texas, Fall, and Rucker Creeks
     Follows the logic from CS3_I_LCBRF_Rev2022G.xlsm

     Parameters
     ----------
     Returns
     -------
     df_unimpaired: dataframe
         Unpaired flow for current station
     """
    # NOTE: This one is different than anything else
    df_ferc_factors = pd.read_csv("./Inputs/FERC-Factors.csv", index_col="Location")
    df_ferc_hydrology = pd.read_csv("./Inputs/FERC-Unit-Hydrology.csv")
    df_ferc_hydrology.index = pd.to_datetime(df_ferc_hydrology.Date)
    df_hydrology = df_ferc_hydrology.loc[
        :"2008-09-30",
        ["5-6000 ft", "6-7000 ft", "7-8000 ft", "8000+ ft"]
    ]
    sl_flows = [
        "Fuller Lake - Local", "Blue Lake - Local", "Rucker Lake",
        "Rucker Creek above Diversion Dam", "Rucker Creek above SYR",
        "Feeley Lake Local", "Carr Lake", "Fall Creek above Lake Creek",
        "Fall Creek above Diversion Dam", "Clear Creek above Diversion Dam",
        "Clear Creek above Fall Creek", "Trap Creek above Diversion Dam",
        "Trap Creek above Fall Creek", "Fall Creek above SYR", "Upper Rock Lake Local",
        "Lower Rock Lake", "Texas Ck above Lindsey Creek", "Culbertson Lake Local",
        "Upper Lindsey Lake Local", "Middle Lindsey Lake", "Lower Lindsey Lake",
        "Lindsey Ck above Texas Creek", "Texas Ck above Diversion Dam",
        "Texas Creek above Canyon Creek"
    ]
    df_selection = df_ferc_factors.loc[sl_flows,:]
    df_factors = df_selection.loc[:, ["5-6000 ft", "6-7000 ft", "7-8000 ft", "8000+ ft"]]
    df_total = df_selection.loc[:, "Precip\nor\nGage volume differences"]

    def calculate_daily_flow(df_row):
        # this logic comes from the FERC Daily Hydrology sheet
        df_flow_calcs = (df_row * df_factors).T.sum() * df_total
        sl_extra = [
            "Rucker Creek above SYR", "Trap Creek above Fall Creek",
            "Fall Creek above SYR", "Texas Creek above Canyon Creek"
        ]
        df_flow_calcs.loc[sl_extra] += df_ferc_hydrology.loc[
            df_row.name, "Pilot Creek below 5000 ft"
        ] * df_selection.loc[
            sl_extra, "Below 5000 ft"
        ] * df_selection.loc[
            sl_extra, "Precip\nor\nGage volume differences.1"
        ]
        return df_flow_calcs.sum()

    df_ferc_daily = df_hydrology.apply(calculate_daily_flow, axis=1)
    # monthly mean and convert to TAF
    df_ferc_monthly = df_ferc_daily.groupby(df_ferc_daily.index.strftime("%Y-%m")).mean()
    df_ferc_monthly.index = pd.date_range("1975-10-31", "2008-09-30", freq="ME")
    df_ferc_monthly_taf = df_ferc_monthly * df_ferc_monthly.index.day *24*60*60/(220*22*9*1000)
    return df_ferc_monthly_taf
