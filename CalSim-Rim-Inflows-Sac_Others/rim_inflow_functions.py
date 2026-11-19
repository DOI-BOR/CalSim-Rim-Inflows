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
import numpy as np
from extension_functionsV2 import create_final_flow_plots, area_scale, remove_negatives_timeseries
from datetime import datetime



def I_EPARK(df_extended_data, df_rim_inflows):
 
    df_location = df_extended_data['Epark']
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_EPARK'] = df_location
    create_final_flow_plots(df_location, list(range(1922, 2021)), 'I_EPARK')

def I_SGRGE(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['SGRGE_IN']
    df_location = remove_negatives_timeseries(df_location.to_frame('temporary'))['temporary']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_SGRGE'] = df_location
    create_final_flow_plots(df_location, list(range(1922, 2021)), 'I_SGRGE')
       
def I_ANT011(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11379000']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_ANT011'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_ANT011')

def I_MLC006(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11381500']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_MLC006'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_MLC006')

def I_DRC012(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11383500']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_DRC012'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_DRC012')

def I_SHSTA(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['SHA']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_SHSTA'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_SHSTA')

def I_COW014 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11374000'] * 0.915    ####  account for differences in drainage area at the gauge location (USGS 11374000) and at the outflow point for the upstream rim watershed.
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_COW014'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_COW014')

def I_BTL006 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11376550']   ####  account for differences in drainage area at the gauge location (USGS 11374000) and at the outflow point for the upstream rim watershed.
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BTL006'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_BTL006')
    
def I_PYN001 (df_extended_data, df_rim_inflows):
    df_location = df_extended_data['11377500'] * 1.1    ####  account for differences in drainage area at the gauge location (USGS 11377500) and at the outflow point for the upstream rim watershed.
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_PYN001'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_PYN001')
    
    
def I_ELD027 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11379500']  ####  
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_ELD027'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_ELD027')
    
def I_MNS000 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11379000'] * 2.359  ####  
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_MNS000'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_MNS000')
    
def I_TRNTY (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11525500'] ####  
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_TRNTY'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_TRNTY')
    
def I_THM028 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11382000'] ####  
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_THM028'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_THM028')
    
def I_CLR011 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['WKYTN'] * 0.14 ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_CLR011'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_CLR011')
    
def I_WKYTN (df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11372000'] * 0.86 ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_WKYTN'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_WKYTN')
    
def I_LWSTN (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["LWSTN"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_LWSTN'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_LWSTN')
    
def I_BCC014 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11384000"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BCC014'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_BCC014')
    
def I_BTC048 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11390000"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BTC048'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_BTC048')
    
def I_LCC038 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["A04280"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_LCC038'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_LCC038')
    
def I_CLRLK (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11451000"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_CLRLK'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_CLRLK')
    
def I_PTH070 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11454000"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_PTH070'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_PTH070')
    
def I_BRC003 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11451715"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BRC003'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_BRC003')
    
def I_CCH053 (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["11451760"] * 0.959545455   ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_CCH053'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_CCH053')
    
def I_LDC029(df_rim_inflows):

    df_location = df_rim_inflows['I_LCC038'] * (1.3155 * 0.8937)
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_LDC029'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2025)), 'I_LDC029')     #BLKBT
    
   
def I_BLKBT (df_extended_data, df_rim_inflows):

    df_location = df_extended_data["BLKBT_neg"]  ####
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BLKBT'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2021)), 'I_BLKBT')    
    
def I_INDVL(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11451300']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_INDVL'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2021)), 'I_INDVL')    
    
def I_BCN010(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11374100']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_BCN010'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2021)), 'I_BCN010')


def I_CWD018(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11375810']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_CWD018'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 1986)), 'I_CWD018')

def I_SCW008(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11375870']
    df_location.loc[df_location < 0] = 0
    df_location = df_location.round(2)
    df_rim_inflows['I_SCW008'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 1986)), 'I_SCW008')

def I_HON021(df_extended_data, df_rim_inflows):

    df_location = df_extended_data['11407500']
    #df_location.loc[df_location < 0] = 0
    #df_location = df_location.round(2)   # skip as not applied in excel sheet
    df_rim_inflows['I_HON021'] = df_location
    create_final_flow_plots(df_location, list(range(1964, 2021)), 'I_HON021') 
    
    
    