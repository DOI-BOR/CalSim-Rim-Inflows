import pandas as pd
from extension_functions import unimpaired_flows, get_diversions
import numpy as np
from datetime import datetime



def unimpaired_11391400(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11391400 Little LAST CHANCE Creek Below FRENCHMAN DAM NR CHILCOOT CA. Follows the logic from CS3_I_FREMAN_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11391400: Little LAST CHANCE Creek Below FRENCHMAN DAM NR CHILCOOT CA (what we are unimpairing)
    # CDEC FRD: Frenchman Reservoir Storage
   
    df_unimpaired = unimpaired_flows(df_gauge_data['11391400'],
                                     fl_storages=[df_gauge_data['FRD'].fillna(0)],
                                     fl_additions=[df_gauge_data['FRD_evap'].fillna(0)],
                                     )

    return df_unimpaired

def unimpaired_11404300(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11404300 GRIZZLY C BL DIV DAM CA. Follows the logic from CS3_I_GZL009_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11404300: USGS 11404300 GRIZZLY C BL DIV DAM CA (what we are unimpairing)
    # 11404250: Grizzly Forbay Storage
    # 11404240: GRIZZLY PP NR STORRIE CA
    # 11403700: BUCKS C PH A STORRIE CA
       
    df_unimpaired = unimpaired_flows(df_gauge_data['11404240'],
                                     fl_storages=[df_gauge_data['11404250'].fillna(0)],
                                     fl_additions=[df_gauge_data['11404250_evap'].fillna(0), df_gauge_data['11403700'].fillna(0),df_gauge_data['11404300'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11404240'].fillna(0),df_gauge_data['11404240'].fillna(0)],
                                    )
    return df_unimpaired

def unimpaired_11399500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11399500 NF FEATHER R NR PRATTVILLE CA. Follows the logic from CS3_I_ALMNR_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11399500: USGS 11399500 NF FEATHER R NR PRATTVILLE CA (what we are unimpairing)
    # 11400200: USGS 11400200 ALMANOR-BUTT C TU A OUTLET NR PRATTVILLE CA (abandoned in December 1958)
    # 11400600: USGS 11400600 BUTT VALLEY PH NR PRATTVILLE CA
    # 11399000: USGS 11399000 Storage for Lake ALMANOR at PRATTVILLE 
    # MMW: Storage for MOUNTAIN MEADOWS RESERVOIR (CDEC=MMW)
    df_unimpaired = unimpaired_flows(df_gauge_data['11400600'],
                                     fl_storages=[df_gauge_data['11399000'].fillna(0), df_gauge_data['MMW'].fillna(0)],
                                     fl_additions=[df_gauge_data['11399000_evap'].fillna(0), df_gauge_data['MMW_evap'].fillna(0),df_gauge_data['11399500'].fillna(0),df_gauge_data['11400200'].fillna(0)],
                                     fl_subtractions=[],
                                    )
    return df_unimpaired

def unimpaired_11401112(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401112 NF FEATHER R BL BELDEN DAM CA. Follows the logic from CS3_I_NFF058_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11401112: USGS 11401112 NF FEATHER R BL BELDEN DAM CA (what we are unimpairing)
    # 11403050: USGS 11403050 NF BELDEN PH at BELDEN CA
    # 11399000: USGS 11399000 Storage for Lake ALMANOR at PRATTVILLE 
    # MMW: Storage for MOUNTAIN MEADOWS RESERVOIR (CDEC=MMW)
    # BTV: Storage for BUTT VALLEY RESERVOIR STORAGE (CDEC=BTV)						
    df_unimpaired = unimpaired_flows(df_gauge_data['11403050'],
                                     fl_storages=[df_gauge_data['11399000'].fillna(0), df_gauge_data['MMW'].fillna(0), df_gauge_data['BTV'].fillna(0)],
                                     fl_additions=[df_gauge_data['11399000_evap'].fillna(0), df_gauge_data['MMW_evap'].fillna(0), df_gauge_data['BTV_evap'].fillna(0), df_gauge_data['11401112'].fillna(0)],
                                     fl_subtractions=[],
                                    )
    return df_unimpaired

def unimpaired_11400500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401112 NF FEATHER R BL BELDEN DAM CA. Follows the logic from CS3_I_NFF058_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11400500: USGS 11400500 BUTT C BL ALMANOR-BUTT C TU NR PRATTVILLE CA (what we are unimpairing)
    # 11400000: USGS 11400000 BUTT C AB ALMANOR-BUTT C TU NR PRATTVILLE CA
    # 11400200: USGS 11400200 ALMANOR-BUTT C TU A OUTLET NR PRATTVILLE CA (The tunnel was abandoned in December 1958,the measured flow from 1983 to 2004 is the leakage from Almanor Lake)
    # WALLACK_DITCH: Wallack Ditch, upstream from station USGS 11400500, diverts about 3 ft³/s during each irrigation season into Yellow Creek Basin
   						
    df_unimpaired = unimpaired_flows(df_gauge_data['11400200'],
                                     fl_storages=[],
                                     fl_additions=[df_gauge_data['11400500'], df_gauge_data['WALLACK_DITCH'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11400200'].fillna(0),df_gauge_data['11400200'].fillna(0)],
                                    )
    #df_unimpaired2 = unimpaired_flows(df_gauge_data['11400000'],
    #                                     fl_storages=[],
    #                                     fl_additions=[df_gauge_data['WALLACK_DITCH'].fillna(0)],
    #                                    fl_subtractions=[],
    #                                    )
   # df_unimpaired[datetime(1936,10,31):datetime(1964,9,30)] = df_unimpaired2[datetime(1936,10,31):datetime(1964,9,30)]
    

    return df_unimpaired

def unimpaired_11400000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401112 NF FEATHER R BL BELDEN DAM CA. Follows the logic from CS3_I_NFF058_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11400000: USGS 11400000 BUTT C AB ALMANOR-BUTT C TU NR PRATTVILLE CA
    # WALLACK_DITCH: Wallack Ditch, upstream from station USGS 11400500, diverts about 3 ft³/s during each irrigation season into Yellow Creek Basin
  						
    df_unimpaired = unimpaired_flows(df_gauge_data['11400000'],
                                         fl_storages=[],
                                         fl_additions=[df_gauge_data['WALLACK_DITCH'].fillna(0)],
                                         fl_subtractions=[],
                                        )

    
    

    return df_unimpaired

def unimpaired_11401125(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401125 INDIAN CREEK NEAR BOULDER CREEK GUARD STATION NEAR TAYLORSVILLE CA. Follows the logic from CS3_I_ANTLP_Rev2022F

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11401125: Little LAST CHANCE Creek Below FRENCHMAN DAM NR CHILCOOT CA (what we are unimpairing)
    # CDEC FRD: Frenchman Reservoir Storage
   
    df_unimpaired = unimpaired_flows(df_gauge_data['11401125'],
                                     fl_storages=[df_gauge_data['ANT'].fillna(0)],
                                     fl_additions=[df_gauge_data['ANT_evap'].fillna(0)],
                                     )

    return df_unimpaired

def unimpaired_11401500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401500 INDIAN C NR CRESCENT MILLS CA. Follows the logic from CS3_I_ANTLP_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11401500:  INDIAN C NR CRESCENT MILLS CA (what we are unimpairing)
    # CDEC FRD: Frenchman Reservoir Storage
   
    df_unimpaired = unimpaired_flows(df_gauge_data['11401500'],
                                     fl_storages=[df_gauge_data['ANT'].fillna(0)],
                                     fl_additions=[df_gauge_data['ANT_evap'].fillna(0)],
                                     )

    return df_unimpaired

def unimpaired_11403000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11401500 INDIAN C NR CRESCENT MILLS CA. Follows the logic from CS3_I_EBF001_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11401500:  INDIAN C NR CRESCENT MILLS CA (what we are unimpairing)
    # CDEC FRD: Frenchman Reservoir Storage
   
    df_FTO_CU=0.2*df_gauge_data['FTO_CU'].copy()
    df_unimpaired = unimpaired_flows(df_gauge_data['11403000'],
                                     fl_storages=[df_gauge_data['ANT'].fillna(0)],
                                     fl_additions=[df_gauge_data['ANT_evap'].fillna(0),df_FTO_CU],
                                     )
    

    return df_unimpaired
def unimpaired_11403530(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11403530 BUCKS C BL DIV DAM NR BUCKS LODGE CA. Follows the logic from CS3_I_UBUCK_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11403530: BUCKS C BL DIV DAM NR BUCKS LODGE CA
    # 11404240: GRIZZLY Power Plant Near STORRIE CA
    # 11403450: MILK RANCH CONDUIT AT OUTLET CA
    # 11403500: BUCKS LK NR BUCKS LODGE CA
    # 11403520: LOWER BUCKS LK NR BUCKS LODGE CA

    df_unimpaired = unimpaired_flows(df_gauge_data['11403530'],
                                         fl_storages=[df_gauge_data['11403500'],df_gauge_data['11403520']],
                                         fl_additions=[df_gauge_data['11404240'].fillna(0),df_gauge_data['11403500_evap'],df_gauge_data['11403520_evap']],
                                         fl_subtractions = [df_gauge_data['11403450'].fillna(0)]
                                        )

    
    

    return df_unimpaired

def unimpaired_11394500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11394500 MF FEATHER R NR MERRIMAC CA. Follows the logic from CS3_I_DAVIS_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11394500: MF FEATHER R NR MERRIMAC CA
    # DAV: LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM)
    # FRD: FRENCHMAN DAM STORAGE
    # LLCID_DIV: ESTIMATED LITTLE LAST CHANCE CREEK IRRIGATION DISTRICT DIVERSIONS
    
    df_unimpaired = unimpaired_flows(df_gauge_data['11394500'],
                                         fl_storages=[df_gauge_data['DAV'].fillna(0),df_gauge_data['FRD'].fillna(0)],
                                         fl_additions=[df_gauge_data['LLCID_DIV'].fillna(0),df_gauge_data['DAV_evap'].fillna(0),df_gauge_data['FRD_evap'].fillna(0)],
                                         fl_subtractions = []
                                        )

    
    

    return df_unimpaired

def unimpaired_11394500_A(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11392100 MF FEATHER R NR PORTOLA CA. Follows the logic from CS3_I_MFF087_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11392100: MF FEATHER R NR PORTOLA CA
    # DAV: LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM)
    # FRD: FRENCHMAN DAM STORAGE
    # FTO_CU: CDEC FTO FEATHER RIVER CONSUMPTIVE USE
    # FTT: CDEC FTT IMPORT FROM LITTLE TRUCKEE RIVER
    
    df_FTO_CU = 0.8* df_gauge_data['FTO_CU'].copy()
    df_unimpaired = unimpaired_flows(df_gauge_data['11394500'],
                                         fl_storages=[df_gauge_data['DAV'].fillna(0),df_gauge_data['FRD'].fillna(0)],
                                         fl_additions=[df_gauge_data['DAV_evap'].fillna(0),df_gauge_data['FRD_evap'].fillna(0),df_FTO_CU],
                                         fl_subtractions = [df_gauge_data['FTT']]
                                        )
    return df_unimpaired

def unimpaired_11392100(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11392100 MF FEATHER R NR PORTOLA CA. Follows the logic from CS3_I_MFF087_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11392100: MF FEATHER R NR PORTOLA CA
    # DAV: LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM)
    # FRD: FRENCHMAN DAM STORAGE
    # FTO_CU: CDEC FTO FEATHER RIVER CONSUMPTIVE USE: 80% for Middle Fork Feather and 20% for Antelope Valley in North Fork Feather
    # FTT: CDEC FTT IMPORT FROM LITTLE TRUCKEE RIVER
    
    df_FTO_CU = 0.8* df_gauge_data['FTO_CU'].copy()
    df_unimpaired = unimpaired_flows(df_gauge_data['11392100'],
                                         fl_storages=[df_gauge_data['DAV'].fillna(0),df_gauge_data['FRD'].fillna(0)],
                                         fl_additions=[df_gauge_data['DAV_evap'].fillna(0),df_gauge_data['FRD_evap'].fillna(0),df_FTO_CU],
                                         fl_subtractions = [df_gauge_data['FTT']]
                                        )
    return df_unimpaired

def unimpaired_11391500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11391500 BIG GRIZZLY C AT GRIZZLY VALLEY DAM NR PORTOLA CA. Follows the logic from CS3_I_DAVIS_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11394500: BIG GRIZZLY C AT GRIZZLY VALLEY DAM NR PORTOLA CA
    # DAV: LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM)
    # FRD: FRENCHMAN DAM STORAGE
    # LLCID_DIV: ESTIMATED LITTLE LAST CHANCE CREEK IRRIGATION DISTRICT DIVERSIONS
    
    df_unimpaired = unimpaired_flows(df_gauge_data['11391500'],
                                         fl_storages=[df_gauge_data['DAV'].fillna(0)],
                                         fl_additions=[df_gauge_data['DAV_evap'].fillna(0)],
                                         fl_subtractions = []
                                        )
    return df_unimpaired
    

def unimpaired_11406500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11391500 BIG GRIZZLY C AT GRIZZLY VALLEY DAM NR PORTOLA CA. Follows the logic from CS3_I_DAVIS_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """
    # 11406500: WB FEATHER R NR YANKEE HILL CA
    # S_RVPHB: Round Valley Lake and Philbrook Lake STORAGE (GRIZZLY VALLEY DAM)
    # FRD: FRENCHMAN DAM STORAGE
    # LLCID_DIV: ESTIMATED LITTLE LAST CHANCE CREEK IRRIGATION DISTRICT DIVERSIONS
    
    df_unimpaired = unimpaired_flows(df_gauge_data['11406500'],
                                         fl_storages=[df_gauge_data['S_RVPHB']],
                                         fl_additions=[df_gauge_data['RVPHB_evap'].fillna(0),df_gauge_data['11389800'],df_gauge_data['MIC']],
                                         fl_subtractions = []
                                        )
   
   
    return df_unimpaired

def unimpaired_11403200(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11403200 NF FEATHER R BL ROCK C DIV DAM CA. Follows the logic from CS3_I_NFF058_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11403200: USGS 11403200 NF FEATHER R BL ROCK C DIV DAM CA  (what we are unimpairing)
    # 11399000: USGS 11399000 Storage for Lake ALMANOR at PRATTVILLE 
    # MMW: Storage for MOUNTAIN MEADOWS RESERVOIR (CDEC=MMW)
    # BTV: Storage for BUTT VALLEY RESERVOIR STORAGE (CDEC=BTV)
    # ANT: Storage for ANTELOPE LAKE STORAGE (CDEC=ANT)		

    df_FTO_CU = 0.2* df_gauge_data['FTO_CU'].copy()	   		
    df_unimpaired = unimpaired_flows(df_gauge_data['11403200'],
                                     fl_storages=[df_gauge_data['11399000'].fillna(0), df_gauge_data['MMW'].fillna(0), df_gauge_data['BTV'].fillna(0), df_gauge_data['ANT'].fillna(0)],
                                     fl_additions=[df_gauge_data['11399000_evap'].fillna(0), df_gauge_data['MMW_evap'].fillna(0), df_gauge_data['ANT_evap'].fillna(0),df_gauge_data['BTV_evap'].fillna(0), df_gauge_data['11403800'].fillna(0),df_FTO_CU],
                                     fl_subtractions=[],
                                    )
    
    return df_unimpaired

def unimpaired_11404500(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11404500 NF FEATHER R A PULGA CA. Follows the logic from CS3_I_NFF029_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11404500: USGS 11404500 NF FEATHER R A PULGA CA  (what we are unimpairing)
    # 11404900: USGS 11404900 POE PH BL POE DAM NR JARBO GAP CA 
    # MMW: Storage for MOUNTAIN MEADOWS RESERVOIR (CDEC=MMW)
    # BTV: Storage for BUTT VALLEY RESERVOIR STORAGE (CDEC=BTV)
    # ANT: Storage for ANTELOPE LAKE STORAGE (CDEC=ANT)		

    df_FTO_CU = 0.2* df_gauge_data['FTO_CU'].copy()	   		
    df_unimpaired = unimpaired_flows(df_gauge_data['11404500'],
                                     fl_storages=[df_gauge_data['11399000'], df_gauge_data['MMW'], df_gauge_data['BTV'], df_gauge_data['ANT'],df_gauge_data['11403500'],df_gauge_data['11403520'].fillna(0),df_gauge_data['11404250'].fillna(0)],
                                     fl_additions=[df_gauge_data['11399000_evap'], df_gauge_data['MMW_evap'], df_gauge_data['ANT_evap'],df_gauge_data['BTV_evap'], df_gauge_data['11403500_evap'],df_gauge_data['11403520_evap'].fillna(0),df_gauge_data['11404250_evap'].fillna(0),df_gauge_data['11404900'],df_FTO_CU],
                                     fl_subtractions=[],
                                    )
    
    return df_unimpaired

def unimpaired_11395030(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11395030 South Fork Feather River below Little Grass Valley Dam 

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11395030: South Fork Feather River below Little Grass Valley Dam (what we are unimpairing)
    # 11395020: LITTLE GRASS VALLEY RESERVOIR NEAR LA PORTE, CA


    df_unimpaired = unimpaired_flows(df_gauge_data['11395030'],
                                     fl_storages=[df_gauge_data['11395020'].fillna(0)],
                                     fl_additions=[df_gauge_data['11395020_evap'].fillna(0)],
                                     )

    return df_unimpaired

def unimpaired_11396000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11396000 LOST C NR CLIPPER MILLS, CA 

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    #primary function when all three are available
    df_unimpaired = unimpaired_flows(df_gauge_data['11396000'],
                                     fl_storages=[df_gauge_data['11395400'].fillna(0)],
                                     fl_additions=[df_gauge_data['11395500'], df_gauge_data['11396090'], df_gauge_data['11395400_evap'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11395150'], df_gauge_data['11413250']],
                                     )
    
    return df_unimpaired

def unimpaired_11395200(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11395200 SOUTH FORK FEATHER RIVER BELOW DIVERSION DAM NR STRAWBERRY VALLEY, CA 

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    df_unimpaired = unimpaired_flows(df_gauge_data['11395200'],
                                     fl_storages=[df_gauge_data['11395020'].fillna(0)],
                                     fl_additions=[df_gauge_data['11395020_evap'].fillna(0), df_gauge_data['11395150']]
                                     )


    return df_unimpaired

def unimpaired_11397000(df_gauge_data):
    """
    Calculate the unimpaired flow for USGS 11397000 SF FEATHER R A ENTERPRISE CA

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------
    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    #primary function when all three are available
    df_unimpaired = unimpaired_flows(df_gauge_data['11397000'],
                                     fl_storages=[df_gauge_data['11395020'].fillna(0), df_gauge_data['11395400'].fillna(0)],
                                     fl_additions=[df_gauge_data['11395020_evap'].fillna(0), df_gauge_data['11395400_evap'].fillna(0), 
                                                   df_gauge_data['11396500'].fillna(0), df_gauge_data['11396310'].fillna(0), df_gauge_data['11395500'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11413250'].fillna(0)]
                                     )


    return df_unimpaired  

def unimpaired_ORO(df_gauge_data):
    """
    Calculate the unimpaired flow for CALCULATED UNIMPAIRED FLOW AT OROVILLE Reservoir. Follows the logic from CS3_I_OROVL_Rev2025

    Parameters
    ----------
    df_gauge_data: dataframe
        Gauge data that contains the current station and all needed to unimpair the flows. in TAF

    Returns
    -------

    df_unimpaired: dataframe
        Unpaired flow for current station
    """

    # 11407000: USGS 11407000 FEATHER RIVER AT OROVILLE CA
    # 11396329: USGS 11396329 KELLY RIDGE PH NR OROVILLE CA
    # ORO: CDEC ORO OROVILLE DAM INFLOW
    # OCO: OCO REPORT OF OPERATIONS OROVILLE DAM INFLOW
    # ORO_INflow: Inflow to Oroville Reservoir
    # 11396310: USGS 11396310 MINERS RANCH CANAL BELOW PONDEROSA DAM NEAR FORBESTOWN CA
    # 11395500: USGS 11395500 OROVILLE WYANDOTTE CANAL NEAR CLIPPER MILLS CA
    # 11396500: USGS 11396500 PALERMO CN A ENTERPRISE  CA (before construction of Lake Oroville)
    # 11389800: USGS 11389800 Toadtown Canal above Butte Canal near Stirling City (Hendricks Canal)
    # MIC: CDEC MIC MIOCENE CANAL DIVERSION (Miocene+Wilenor Canals)
    # 11413250: USGS 11413250 SLATE CREEK TUNNEL NEAR STRAWBERRY VALLEY CA
    # FTO_CU: CDEC FTO FEATHER RIVER CONSUMPTIVE USE
    # 11399000: USGS 11399000 LAKE ALMANOR AT PRATTVILLE 
    # MMW: CDEC MMW MOUNTAIN MEADOWS RESERVOIR
    # 11403520: USGS 11403520 LOW BUCKS LAKE NEAR BUCKS LODGE CA
    # 11403500: USGS 11403500 BUCKS LAKE NEAR BUCKS LODGE CA
    # BTV: CDEC BTV, BUTT VALLEY RESERVOIR STORAGE 
    # ANT: CDEC ANT: ANTELOPE LAKE STORAGE
    # 11404250: USGS 11404250 GRIZZLY FOREBAY NR STORRIE CA
    # 11395020: USGS 11395020 LITTLE GRASS VALLEY RESERVOIR NEAR LA PORTE, CA
    # 11395400:SLY CREEK RESERVOIR NEAR STRAWBERRY VALLEY, CA
    # FRD: CDEC FRD, FRENCHMAN DAM STORAGE
    # DAV: CDEC DAV, LAKE DAVIS STORAGE (GRIZZLY VALLEY DAM)
    # RVPHB: PG&E COMBINED ROUND VALLEY AND PHILBROOK RESERVOIRS


    df_unimpaired = unimpaired_flows(df_gauge_data['ORO_Inflow'],
                                     fl_storages=[df_gauge_data['11399000'].fillna(0), df_gauge_data['MMW_EX'].fillna(0), df_gauge_data['11403520'].fillna(0), df_gauge_data['11403500'].fillna(0),
                                                  df_gauge_data['BTV'].fillna(0), df_gauge_data['ANT'].fillna(0), df_gauge_data['11404250'].fillna(0), df_gauge_data['FRD'].fillna(0),
                                                  df_gauge_data['DAV'].fillna(0), df_gauge_data['S_RVPHB'].fillna(0),df_gauge_data['11395020'].fillna(0),df_gauge_data['11395400'].fillna(0)],
                                     fl_additions=[df_gauge_data['11399000_evap'].fillna(0), df_gauge_data['MMW_EX_evap'].fillna(0), df_gauge_data['11403520_evap'].fillna(0),
                                                   df_gauge_data['11403500_evap'].fillna(0), df_gauge_data['BTV_evap'].fillna(0), df_gauge_data['ANT_evap'].fillna(0),
                                                   df_gauge_data['11404250_evap'].fillna(0), df_gauge_data['FRD_evap'].fillna(0), df_gauge_data['DAV_evap'].fillna(0),
                                                   df_gauge_data['RVPHB_evap'].fillna(0), df_gauge_data['11395020_evap'].fillna(0),df_gauge_data['11395400_evap'].fillna(0),df_gauge_data['11396310'].fillna(0), df_gauge_data['11395500'].fillna(0),
                                                  df_gauge_data['11389800'].fillna(0), df_gauge_data['11396500'].fillna(0),df_gauge_data['MIC'].fillna(0), df_gauge_data['FTO_CU'].fillna(0)],
                                     fl_subtractions=[df_gauge_data['11413250'].fillna(0)])

    
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

