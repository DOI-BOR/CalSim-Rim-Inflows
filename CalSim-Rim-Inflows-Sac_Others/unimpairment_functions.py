######################################################
#### DWR MSO OFFICE                                ###
#### Calsim Data Extention - Rim Watershed Project ###
#### Region : "Sacramento Other"                   ###
########################################################################################################
## Rim Inflow:                                                                                       ###
## I_SHSTA  : x                      #I_COW014 : x                             #I_BCN010 : x         ###
## I_BTL006 : x                      #I_PYN001 : x                             #I_ANT011 : x         ###
## I_MNS000 : x                      #I_TRNTY  : x                             #I_WKYTN  : x         ###
## I_SCW008 : x                      #I_ELD027 : x                             #I_THM028 : x         ###
## I_BLKBT  : x                      #I_SGRGE  : x                             #I_EPARK  : x         ###
## I_INDVL  : x                      #I_CCH053 : x                             #I_PTH070 : x         ###                      
## I_LWSTN  : x                      #I_CLR011 : x                             #I_CWD018 : x         ###
## I_BCC014 : x                      #I_BTC048 : x                             #I_LCC038 : x         ###
## I_CLRLK  : x                      #I_BRC003 : x                             #I_LDC029 : x         ###
## I_HON021 : x                      #I_MLC006 : x                             #I_DRC012 : x         ###
########################################################################################################

import pandas as pd
from extension_functionsV2 import unimpaired_flows, get_diversions,remove_negatives,remove_negatives_timeseries
import numpy as np
from datetime import datetime



def unimpaired_11374100(df_gauge_data):  #I_BCN010
    """
    Calculate the unimpaired flow for USGS 11374100  Bear Creek near Millville   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11374100'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11375810(df_gauge_data):  # I_CWD018
    """
    Calculate the unimpaired flow for USGS 11375810  Cottonwood Creek near Olinda   - No reservior

    """

    df_unimpaired = unimpaired_flows(df_gauge_data['11375810'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11375870(df_gauge_data):  #I_SCW008
    """
    Calculate the unimpaired flow for USGS 11375870  SF Cottonwood Creek near Olinda   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11375870'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11379500(df_gauge_data):   #I_ELD027
    """
    Calculate the unimpaired flow for USGS 11379500  Elder Creek near Paskenta   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11379500'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11390000(df_gauge_data):  #I_BTC048
    """
    Calculate the unimpaired flow for USGS 11390000  Butte Creek near Chico   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11390000'], fl_subtractions=[df_gauge_data['11389800'].fillna(0)])   ### no reservior - no ET
    return df_unimpaired

def unimpaired_Epark(df_gauge_data):  #I_EPARK
    """
    Calculate the unimpaired flow for inflow to Epark   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['Epark'])   ### no reservior - no ET
    return df_unimpaired

def unimpaired_SGRGE_IN(df_gauge_data):  #I_SGRGE
    """
    Calculate the unimpaired flow for SGRGE Inflow - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['SGRGE_IN'], fl_subtractions=[df_gauge_data['EPARK_RE'].fillna(0)])   ### no reservior - no ET
    return df_unimpaired


def unimpaired_11407500(df_gauge_data):   #I_HON021
    """
    Calculate the unimpaired flow for USGS 11407500  S HONCUT C NR BANGOR CA   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11407500'])   ### no reservior - no subtraction - no evaporation
    return df_unimpaired


def unimpaired_11379000(df_gauge_data):   #I_ANT011
    """
    Calculate the unimpaired flow for USGS 11379000  Antelope Creek near Red Bluff   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11379000'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11381500(df_gauge_data):  #I_MLC006
    """
    Calculate the unimpaired flow for USGS 11381500   Mill Creek near Los Molinos   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11381500'])   ### no reservior - no subtraction - no ET
    return df_unimpaired
    
def unimpaired_11383500(df_gauge_data):  #I_DRC012
    """
    Calculate the unimpaired flow for USGS 11383500   Deer Creek near Vina   - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11383500'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_SHA(df_gauge_data):   #I_SHSTA
    """
    Calculate the unimpaired flow for Lake shasta Resevoir

    """
    ###  (1942 - 1944)
    #Sacramento River at Keswick minus 1.8 percent of the accretion between Sacramento River at Keswick and Sacramento River at Red Bluff
    #plus any increase in Shasta Lake storage plus reservoir evaporation.  (1942 - 1944)
    #primary function when all three are available
    #df_accretion1 = df_gauge_data.loc["1942-10-01":"1943-12-31",'11378000'] - df_gauge_data.loc["1942-10-01":"1943-12-31","11370500"]   #   
    df_accretion1 = df_gauge_data['11378000'] - df_gauge_data["11370500"]                
    df_accretion1[df_accretion1 < 0] = 0
    df_accretion1 = 0.018 * df_accretion1
    
    df_unimpaired = unimpaired_flows(df_gauge_data['11370500'],   
                                     fl_storages=[df_gauge_data['SHA'].fillna(0)],       
                                     fl_additions=[df_gauge_data['SHA_evap'].fillna(0)],  
                                     fl_subtractions=[df_accretion1.fillna(0)],#
                                     )
    ###  (1921 - 1925)
    #•	October 1921 to September 1925: 1957 Joint Hydrology Study.
    df_unimpaired.loc[:"1925-09-30"] = (df_gauge_data.loc[:"1925-09-30", '1957-JHS-Shsta'])
    
    ###•	October 1925 to September 1942
    #Sacramento River at Kennett plus 2.5 percent of the accretion 
    #between Sacramento River at Kennett and Sacramento River at Red Bluff.
    
    df_accretion2 = df_gauge_data['11378000'] - df_gauge_data["11369500"]                
    df_accretion2[df_accretion2 < 0] = 0
    df_accretion2 = 0.025 * df_accretion2
    Kennett = df_gauge_data["11369500"]  + df_accretion2
    df_unimpaired.loc["1925-10-01":"1942-09-30"] = Kennett.loc["1925-10-01":"1942-09-30"]
    
    # January 1944 to current: Reclamation reports of reservoir operations.
    df_unimpaired.loc["1944-01-01":] = (df_gauge_data.loc["1944-01-01":, 'Reservoir-Ops-Shsta'])
    
    return df_unimpaired

def unimpaired_11374000(df_gauge_data):   #I_COW014
    """
    Calculate the unimpaired flow for USGS 11374000   Cow Creek near Millville    - No reservior

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11374000'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11376550(df_gauge_data):  #I_BTL006
    """
    Calculate the unimpaired flow for   Battle Creek  - No Storage

    """
    # 1922-1940  regression with Mill creek
    # 1941-1961   USGS 11376500 BATTLE C NR COTTONWOOD  CA (Gaged flows do not include diversions to fish hatchery (estimated to be 60 cfs year round))
    days_in_month = df_gauge_data.index.days_in_month
    fish_hatchery_div =   pd.Series(60 * days_in_month * 0.00198347,index=df_gauge_data.index)   # cfs to TAF
    df_unimpaired = unimpaired_flows(df_gauge_data['11376500'],   #       #
                                     fl_additions=[fish_hatchery_div])
    
    df_unimpaired.loc["1961-10-31":] = (df_gauge_data.loc["1961-10-31":, '11376550'])
    return df_unimpaired

def unimpaired_11377500(df_gauge_data):    #I_PYN001
    """
    Calculate the unimpaired flow for USGS 11377500 PAYNES C NR RED BLUFF  CA - No Storage

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11377500'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_MNS(df_gauge_data):       # I_MNS000   - no need- dependent on other 
    """
    Calculate the unimpaired flow for Minor Northeast Streams- No gauge data

    """

def unimpaired_11525500(df_gauge_data):  # I_TRNTY and I_LWSTN
    """
    Calculate the unimpaired flow for USGS 11525500 TRINITY R A LEWISTON C (used for both Trinity inflow and Lewistion Inflow)

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11525500'],
                                     fl_storages=[df_gauge_data['CLE'].fillna(0),df_gauge_data['LEW'].fillna(0)],
                                     fl_additions=[df_gauge_data['CLE_evap'].fillna(0),df_gauge_data['LEW_evap'].fillna(0),df_gauge_data['11525430'].fillna(0)])
      
    return df_unimpaired

def unimpaired_11382000 (df_gauge_data):   # I_THM028
    """
    Calculate the unimpaired flow for USGS 11382000 THOMES C A PASKENTA CA- No Storage

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11382000'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_11372000(df_gauge_data):   # I_CLR011  and   I_WKYTN
    """
    Calculate the unimpaired flow for USGS 11372000 CLEAR CK NR IGO CA   AND whiskeytown

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11372000'].clip(lower=0),
                                     fl_storages=[df_gauge_data['WHI'].fillna(0).clip(lower=0)],
                                     fl_additions=[df_gauge_data['WHI_evap'].fillna(0).clip(lower=0),df_gauge_data['Whiskeytown Deliveries'].fillna(0).clip(lower=0),df_gauge_data['11371600'].fillna(0).clip(lower=0)],
                                     fl_subtractions=[df_gauge_data['11525430'].fillna(0).clip(lower=0)])

    return df_unimpaired

def unimpaired_11384000(df_gauge_data):   # I_BCC014
    """
    Calculate the unimpaired flow for USGS 11384000 BIG CHICO C NR CHICO CA- No Storage

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11384000'])   ### no reservior - no subtraction - no ET
    return df_unimpaired

def unimpaired_A04280(df_gauge_data):    # I_LCC038 and I_LDC029
    """
    Calculate the unimpaired flow for DWR A04280 Little Chico Creek near Chico - No Storage

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['A04280'],fl_additions=[df_gauge_data['Div-A04910'].fillna(0)])   
    return df_unimpaired

def unimpaired_11451000(df_gauge_data):   # I_CLRLK
    """
    Calculate the unimpaired flow for USGS 11451000 CACHE C NR LOWER LAKE CA

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11451000'],
                                     fl_storages=[df_gauge_data['ClearLake'].fillna(0)],
                                     fl_additions=[df_gauge_data['11451000_evap'].fillna(0)])   
    return df_unimpaired

def unimpaired_11454000(df_gauge_data):   #I_PTH070 and 
    """
    Calculate the unimpaired flow for  Putah creek

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['11454000'],
                                     fl_storages=[df_gauge_data['11453900'].fillna(0).clip(lower=0)],
                                     fl_additions=[df_gauge_data['11453900_evap'].fillna(0),df_gauge_data['PTH-Upstream-Depletion'].fillna(0)])   
    return df_unimpaired

def unimpaired_BRE(df_gauge_data):     # I_BRC003
    """
    Calculate the unimpaired flow for LK BERRYESSA

    """
    df_unimpaired = unimpaired_flows(df_gauge_data['BERRYESSA-RELEASE'],  # BERRYESSA-RELEASE' from cdec
                                     fl_storages=[df_gauge_data['11453900'].fillna(0)],
                                     fl_additions=[df_gauge_data['11453900_evap'].fillna(0),df_gauge_data['PTH-Upstream-Depletion'].fillna(0)])   
    return df_unimpaired

def unimpaired_BLKBT(df_gauge_data):   # I_BLKBT
    """
    Calculate the unimpaired flow for Local inflow to Black Butte Reservoir

    """
    df_unimpaired = df_gauge_data['BlackButte_IN'] - df_gauge_data['SGRGE_RE']  
    return df_unimpaired

def unimpaired_11451300(df_gauge_data):    #I_INDVL
    """
    Calculate the unimpaired flow for USGS 11451300  NF Cache C NR Clear Lake Oaks CA 

    """  
    df_unimpaired = unimpaired_flows(df_gauge_data['11451300'],
                                     fl_storages=[df_gauge_data['INV'].fillna(0)],
                                     fl_additions=[df_gauge_data['INDVL_evap'].fillna(0)])  
    return df_unimpaired



