######################################################
#### DWR MSO OFFICE                                ###
#### Calsim Data Extention - Rim Watershed Project ###
#### Region : "Sacramento Other"                   ###
########################################################################################################
## Rim Inflow:                                                                                       ###
## I_SHSTA  : c                      #I_COW014 : Note                          #I_BCN010 : c         ###
## I_BTL006 : c                      #I_PYN001 : c                             #I_ANT011 : c         ###
## I_MNS000 : c                      #I_TRNTY  : c                             #I_WKYTN  : Note      ###
## I_SCW008 : c                      #I_ELD027 : c                             #I_THM028 : c         ###
## I_BLKBT  : Note                   #I_SGRGE  : c                             #I_EPARK  : c         ###
## I_INDVL  : c                      #I_CCH053 : Note                          #I_PTH070 : Note      ###                      
## I_LWSTN  : c                      #I_CLR011 : c                             #I_CWD018 : c         ###
## I_BCC014 : c                      #I_BTC048 : c                             #I_LCC038 : c         ###
## I_CLRLK  : Note                   #I_BRC003 : Note                          #I_LDC029 : x         ###
## I_HON021 : c                      #I_MLC006 : c                             #I_DRC012 : c         ###
########################################################################################################

from extension_functionsV2 import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    
    i_final_year = 2021
    s_evap_dss_path = "./Inputs/evaporation_rates.dss"
    b_compareData = True
    s_prev_rim_inflows_fn = r".\SVInput\Spreadsheet_SVInput.xlsm" 
    s_prev_rim_inflow_sheet = "Inflows" 
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)
    df_full_data = pd.read_csv('./Intermediate/Sacramento_other_full_gauge_data.csv', index_col=0, parse_dates=True)
    df_full_data.to_csv('./Intermediate/Sacramento_other_full_gauge_data_gap_filled.csv')
    df_unimpaired_data = pd.DataFrame()
    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()
    df_rim_inflows = pd.DataFrame()

    ###############################################################################
    print("Calculating evaporation...")
    ###############################################################################
    calc_evap_SHA(s_evap_dss_path, df_full_data)    
    calc_evap_CLE(s_evap_dss_path, df_full_data)    
    calc_evap_LEW(s_evap_dss_path, df_full_data)    
    calc_evap_WHI(s_evap_dss_path, df_full_data)   
    calc_evap_CLAKE(s_evap_dss_path, df_full_data)  
    calc_evap_BRY(s_evap_dss_path, df_full_data)    
    calc_evap_INDVL(s_evap_dss_path, df_full_data) 
    
    df_full_data.to_csv('./Intermediate/Sacramento_other_full_gauge_data_wevap.csv')

    
    

    ###############################################################################
    print("Calculating unimpaired flows...")  
    ###############################################################################
    df_unimpaired_data['11374100'] = unimpaired_11374100(df_full_data)      # I_BCN010
    df_unimpaired_data['11375810'] = unimpaired_11375810(df_full_data)      # I_CWD018
    df_unimpaired_data['11375870'] = unimpaired_11375870(df_full_data)      # I_SCW008
    df_unimpaired_data['11379500'] = unimpaired_11379500(df_full_data)      # I_ELD027
    df_unimpaired_data['11390000'] = unimpaired_11390000(df_full_data)      # I_BTC048
    df_unimpaired_data['Epark']    = unimpaired_Epark(df_full_data)         # I_EPARK
    df_unimpaired_data['SGRGE_IN'] = unimpaired_SGRGE_IN(df_full_data)      # I_SGRGE
    df_unimpaired_data['11407500'] = unimpaired_11407500(df_full_data)      # I_HON021
    df_unimpaired_data['11379000'] = unimpaired_11379000(df_full_data)      # I_ANT011
    df_unimpaired_data['11381500'] = unimpaired_11381500(df_full_data)      # I_MLC006
    df_unimpaired_data['11383500'] = unimpaired_11383500(df_full_data)      # I_DRC012
    df_unimpaired_data['SHA']      = unimpaired_SHA(df_full_data)           # I_SHSTA
    df_unimpaired_data['11374000'] = unimpaired_11374000(df_full_data)      # I_COW014
    df_unimpaired_data['11376550'] = unimpaired_11376550(df_full_data)      # I_BTL006
    df_unimpaired_data['11377500'] = unimpaired_11377500(df_full_data)      # I_PYN001
    df_unimpaired_data['11525500'] = unimpaired_11525500(df_full_data)      # I_TRNTY / I_LWSTN
    df_unimpaired_data['11382000'] = unimpaired_11382000(df_full_data)      # I_THM028
    df_unimpaired_data['11372000'] = unimpaired_11372000(df_full_data)      # I_CLR011 / I_WKYTN
    df_unimpaired_data['11384000'] = unimpaired_11384000(df_full_data)      # I_BCC014
    df_unimpaired_data['A04280']   = unimpaired_A04280(df_full_data)        # I_LCC038 / I_LDC029
    df_unimpaired_data['11451000'] = unimpaired_11451000(df_full_data)      # I_CLRLK
    df_unimpaired_data['11454000'] = unimpaired_11454000(df_full_data)      # I_PTH070
    df_unimpaired_data['BRE']      = unimpaired_BRE(df_full_data)           # I_BRC003
    df_unimpaired_data['BLKBT']    = unimpaired_BLKBT(df_full_data)         # I_BLKBT
    df_unimpaired_data['11451300'] = unimpaired_11451300(df_full_data)      # I_INDVL
    
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)
    df_unimpaired_data.to_csv('./Intermediate/Sacramento_other_unimpaired_data.csv')
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)
    df_pos_unimpaired_data.to_csv('./Intermediate/Sacramento_other_unimpaired_data_pos.csv')


    ###############################################################################
    print("Extending flows...")
    ###############################################################################
      # I_ANT011
    extend_data(df_full_data['11381500'], df_pos_unimpaired_data['11379000'],  df_extended_data, df_synthetic_data, 1941, 1982, True, '11379000', i_final_year=i_final_year, exclude_from_regression=list(range(1921, 1941)) ) 
    
    # I_MLC006
    extend_data(df_full_data['11383500'], df_pos_unimpaired_data['11381500'],  df_extended_data, df_synthetic_data, 1929, 2021, False, '11381500', i_final_year=i_final_year,exclude_from_regression=list(range(1921, 1929)) )   
    
    # I_DRC012   ## No synthetic data - all historical 11383500
    df_extended_data["11383500"] = df_pos_unimpaired_data['11383500']
    
    # I_SHSTA    ## No synthetic data - all historical  SHA'   
    df_extended_data["SHA"] = df_pos_unimpaired_data['SHA']
    
    # I_COW014   #  excel should should rerun and the be used
    extend_data(df_full_data['11381500'], df_pos_unimpaired_data['11374000'],  df_extended_data, df_synthetic_data, 1950, 2021, True, '11374000', i_final_year=i_final_year )  
    
    # I_BTL006
    extend_data(df_full_data['11381500'], df_pos_unimpaired_data['11376550'],  df_extended_data, df_synthetic_data, 1941, 2021, True, '11376550', i_final_year=i_final_year) 
    
    # I_PYN001 
    extend_data(df_full_data['11381500'], df_pos_unimpaired_data['11377500'],  df_extended_data, df_synthetic_data, 1950, 1966, True, '11377500', i_final_year=i_final_year)  
    
    # I_MNS000 (dependent)  use  (Antelope Creek near Red Bluff) -
    
    # I_TRNTY - first combine observed lake inflow with unimpaired  and the do regression                                                                                                                   
    df_full_data['TRINITY LAKE INFLOW'] = df_full_data['TRINITY LAKE INFLOW'].clip(lower=0).combine(df_pos_unimpaired_data['11525500'], min)
    extend_data(df_pos_unimpaired_data['11525500'], df_full_data['TRINITY LAKE INFLOW'],  df_extended_data, df_synthetic_data, 1962, 2021, True, '11525500', i_final_year=i_final_year)   
    
    # I_THM028
    extend_data(df_full_data['11376000'], df_pos_unimpaired_data['11382000'],  df_extended_data, df_synthetic_data, 1941, 1996, True, '11382000', i_final_year=i_final_year, exclude_from_regression=list(range(1921, 1941)) )
    
    # I_CLR011  ## cvp dlecieris should extend manually
    extend_data(df_full_data['11382000'], df_unimpaired_data['11372000'],  df_extended_data, df_synthetic_data, 1941, 1996, True, '11372000', i_final_year=1996, exclude_from_regression=list(range(1921, 1941)))
    df_extended_data.loc["1996-10-31":"2021-09-30", '11372000'] = (df_unimpaired_data.loc["1996-10-31":"2021-09-30", '11372000'])
    df_extended_data["11372000"] = remove_negatives_timeseries(df_extended_data[["11372000"]])
    
    # I_WKYTN  (dependent)   use unimpaired USGS 11372000 CLEAR CK NR IGO CA 
    extend_data(df_full_data['11382000'], df_unimpaired_data['11372000'],  df_extended_data, df_synthetic_data, 1941, 2021, True, 'WKYTN', i_final_year=1996, exclude_from_regression=list(range(1921, 1941)))
    df_extended_data.loc["1996-10-31":"2021-09-30", 'WKYTN'] = (df_unimpaired_data.loc["1996-10-31":"2021-09-30", '11372000'])
    df_extended_data["WKYTN"] = remove_negatives_timeseries(df_extended_data[["11372000"]])
    
    # I_LWSTN    Dependent to Trinity   # use  USGS 11525500 TRINITY R A LEWISTON
    df_extended_data["LWSTN"] = df_unimpaired_data['11525500'] - df_extended_data["11525500"]
    df_extended_data["LWSTN"] = remove_negatives_timeseries(df_extended_data[["LWSTN"]])
    
    #I_BCC014  (combination of 3 regression models) - gauge need to extend manually
    extend_data(df_full_data['11383500'], df_pos_unimpaired_data['11384000'],  df_extended_data, df_synthetic_data, 1922, 1986, True, '11384000-A', i_final_year=i_final_year )
    extend_data(df_full_data['Chico-DWR-gauges'], df_pos_unimpaired_data['11384000'],  df_extended_data, df_synthetic_data, 1922, 1986, True, '11384000-B',1976, i_final_year=i_final_year)
    df_extended_data.loc[:"1975-09-30", '11384000-B'] = (df_pos_unimpaired_data.loc[:"1975-09-30", '11384000'])
    extend_data(df_full_data['11383500'], df_full_data['A42105'],  df_extended_data, df_synthetic_data, 1998, 2020, False, '11384000-D', i_final_year=i_final_year, exclude_from_regression=[1997] )
    df_extended_data['11384000'] = pd.concat([df_extended_data.loc[:"1996-09-30", '11384000-B'],df_extended_data.loc["1996-10-31" : "2020-09-30", '11384000-D'],df_extended_data.loc["2020-10-31": , '11384000-A']])
    
    #I_BTC048 -  AllHistorical data
    df_extended_data["11390000"] = df_pos_unimpaired_data['11390000']
    
    #I_LCC038  - for 1969-1972  use max reg model and historical
    extend_data(df_extended_data['11390000'].round(2), df_pos_unimpaired_data['A04280'],  df_extended_data, df_synthetic_data, 1973, 1996, True, 'A04280', i_final_year=i_final_year, exclude_from_regression=list(range(1969, 1973)) )
    df_extended_data.loc["1968-10-31":"1972-09-30", "A04280"] = np.maximum(df_full_data.loc["1968-10-31":"1972-09-30", "A04280"], df_synthetic_data.loc["1968-10-31":"1972-09-30", "A04280"])
    
    #I_CLRLK - All Historical
    df_extended_data["11451000"] = df_pos_unimpaired_data['11451000']
    
    #I_PTH070  - LK BERRYESSA
    df_pos_unimpaired_data_11454000_filled = df_pos_unimpaired_data[["11454000"]]
    df_pos_unimpaired_data_11454000_filled.loc["1921-10-31":"1930-09-30", "11454000"] = df_full_data.loc["1921-10-31":"1930-09-30", "11454500-scaled"]
    extend_data(df_pos_unimpaired_data_11454000_filled['11454000'], df_pos_unimpaired_data['BRE'],  df_extended_data, df_synthetic_data, 1976, 2021, True, '11454000', i_final_year=i_final_year )
    
    # I_BRC003
    df_full_data["df_Bear_Creek_combined"] = df_full_data['11451720'].mul(0.949).add(df_full_data['11451715'], fill_value=0)
    extend_data(df_pos_unimpaired_data["11454000"], df_full_data["df_Bear_Creek_combined"],  df_extended_data, df_synthetic_data, 1998, 2021, False, '11451715',1921, i_final_year=i_final_year, exclude_from_regression=list(range(1981, 1998)) )
    df_extended_data.loc["1958-10-31":"1980-09-30", "11451715"] = df_full_data.loc["1958-10-31":"1980-09-30", "df_Bear_Creek_combined"]
    df_extended_data["11451715"] = remove_negatives_timeseries(df_extended_data[["11451715"]])
    
    # I_CCH053
    df_full_data["cache_creek_capay"] =  df_full_data["11452000"] - df_full_data["11451720"] - df_full_data["11451500"] - df_full_data["11451000"]    # Cache Creek near Capay
    df_full_data["cache_creek_capay"] = remove_negatives_timeseries(df_full_data[["cache_creek_capay"]])
    df_full_data.loc["1971-10-31":"1972-09-30", "cache_creek_capay"] = 0  # manuall adjustment based on excel sheet
    extend_data(df_pos_unimpaired_data["11454000"], df_full_data["cache_creek_capay"],  df_extended_data, df_synthetic_data, 1959, 1972, False, '11451760', i_final_year=i_final_year, exclude_from_regression=list(range(1973, 1977)) )
    df_extended_data.loc["1972-10-31":"1976-09-30", "11451760"] = df_full_data.loc["1972-10-31":"1976-09-30", "cache_creek_capay"]
    df_extended_data.loc["1976-10-31":"1977-09-30", "11451760"] = df_extended_data.loc["1976-10-31":"1977-09-30", "11451760"].clip(lower=0)   #manuall adjustment based on excel sheet
    
    # I_BLKBT
    df_full_data.loc["1921-10-31":"2015-09-30", "EPARK_RE_2015"] = df_full_data.loc["1921-10-31":"2015-09-30", "EPARK_RE"]
    df_full_data["SGRGE_EPARK"] =  df_full_data["SGRGE_IN2"] - df_full_data["EPARK_RE_2015"].fillna(0) + df_full_data["Epark"]   # INFLOWS TO EAST PARK RESERVOIR + STONY GORGE INFLOWS LESS EAST PARK DAM RELEASES
    extend_data(df_full_data["SGRGE_EPARK"].iloc[1:], df_unimpaired_data["BLKBT"],  df_extended_data, df_synthetic_data, 1964, 2021, False, 'BLKBT', i_final_year=i_final_year, exclude_from_regression=list(range(1953, 1964)) )
    df_extended_data["BLKBT_neg"] = remove_negatives_timeseries(df_extended_data[["BLKBT"]])
   
    # I_INDVL
    extend_data(df_full_data['11471500'], df_pos_unimpaired_data['11451300'],  df_extended_data, df_synthetic_data, 1975, 2021, True, '11451300', i_final_year=i_final_year)
    
    # I_EPARK
    df_extended_data.loc["1921-10-31":"2021-09-30", 'Epark'] = (df_pos_unimpaired_data.loc["1921-10-31":"2021-09-30", 'Epark'])
    
    # I_SGRGE
    df_extended_data.loc["1921-10-31":"2021-09-30", 'SGRGE_IN'] = (df_pos_unimpaired_data.loc["1921-10-31":"2021-09-30", 'SGRGE_IN'])
    
    # I_SCW008
    extend_data(df_full_data['11376000'], df_pos_unimpaired_data['11375870'],  df_extended_data, df_synthetic_data, 1978, 1986, True, '11375870', i_final_year=i_final_year) 
    
    # I_BCN010
    extend_data(df_full_data['11381500'], df_pos_unimpaired_data['11374100'],  df_extended_data, df_synthetic_data, 1960, 1967, True, '11374100', i_final_year=i_final_year) 
    
    # I_CWD018
    extend_data(df_full_data['11376000'], df_pos_unimpaired_data['11375810'],  df_extended_data, df_synthetic_data, 1972, 1986, True, '11375810', i_final_year=i_final_year) 
    
    # I_ELD027
    extend_data(df_full_data['11382000'], df_pos_unimpaired_data['11379500'],  df_extended_data, df_synthetic_data, 1949, 2021, True, '11379500', i_final_year=1996) 
    df_extended_data.loc["1996-10-31":"2021-09-30", '11379500'] = (df_pos_unimpaired_data.loc["1996-10-31":"2021-09-30", '11379500'])
    
    # I_HON021
    extend_data(df_extended_data['11390000'].round(2), df_pos_unimpaired_data['11407500'],  df_extended_data, df_synthetic_data, 1951, 1986, False, '11407500', i_final_year=i_final_year)
        
    df_extended_data.to_csv('./Intermediate/upper_feather_extended_data.csv')  
    df_synthetic_data.to_csv('./Intermediate/upper_feather_synthetic_data.csv') 

 
 
    ###############################################################################
    print("Calculating rim inflows...")
    ###############################################################################
    I_SHSTA(df_extended_data, df_rim_inflows)
    I_COW014(df_extended_data, df_rim_inflows)  # excel  macro should be run first to match the output
    I_BCN010(df_extended_data, df_rim_inflows)
    
    I_BTL006(df_extended_data, df_rim_inflows)
    I_PYN001(df_extended_data, df_rim_inflows)
    I_ANT011(df_extended_data, df_rim_inflows)

    I_MNS000(df_extended_data, df_rim_inflows)
    I_TRNTY(df_extended_data, df_rim_inflows)
    I_WKYTN(df_extended_data, df_rim_inflows)  # sourec (CS3_I_CLR011_2020G) in excel sheet is outdated should be CS3_I_CLR011_2022H - cause mismatch

    I_SCW008(df_extended_data, df_rim_inflows)
    I_ELD027(df_extended_data, df_rim_inflows)
    I_THM028(df_extended_data, df_rim_inflows)

    I_BLKBT(df_extended_data, df_rim_inflows)  # # in orginal excel, data d for regression are ones before negative adjustment- cause problem with S-curve dissAg and mismatch
    I_SGRGE(df_extended_data, df_rim_inflows)
    I_EPARK(df_extended_data, df_rim_inflows)

    I_PTH070(df_extended_data, df_rim_inflows) # excel  macro should be run first to match the output
    I_INDVL(df_extended_data, df_rim_inflows)
    I_CCH053(df_extended_data, df_rim_inflows) # in orginal excel, the unimpaired putah creek data used for regression are data before negative adjustment- negative adjustment
    #can cause error in s-curve dissagreggation proccess - the cell refrences should be changed to values after negative-adjustment (start from column AK) , year 1973-1976 replaced by historical values and then result are compareble with code
    
    
    I_LWSTN(df_extended_data, df_rim_inflows)
    I_CLR011(df_extended_data, df_rim_inflows)
    I_CWD018(df_extended_data, df_rim_inflows)
    
    I_BCC014(df_extended_data, df_rim_inflows)
    I_BTC048(df_extended_data, df_rim_inflows)
    I_LCC038(df_extended_data, df_rim_inflows)
    
    I_CLRLK(df_extended_data, df_rim_inflows)  # 10/31/2013 is missed in excel sheet (Redistribution tab) - it should be fixed before comparison
    I_BRC003(df_extended_data, df_rim_inflows) # tab "Unimpaired Putah Creek 11454000" is outdated it should be updated first, run the macro , replace 1959-1980with hist data and then take the output for comparison
    I_LDC029(df_rim_inflows)
    
    I_HON021(df_extended_data, df_rim_inflows)
    I_MLC006(df_extended_data, df_rim_inflows)
    I_DRC012(df_extended_data, df_rim_inflows)
      
    df_rim_inflows.to_csv('./Outputs/Sacramento_other_rim_inflows.csv')

    ###############################################################################
    # Comparison with Previous Rim Inflow dataset
    ###############################################################################
    if b_compareData:

        df_reference = pd.read_excel(s_prev_rim_inflows_fn, sheet_name=s_prev_rim_inflow_sheet, skiprows=[0,2,3,4,5,6,7,8,9,10,11],header=0, index_col=0, parse_dates=True)
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')
        df_diffs['Median Value - Original'] = df_reference[df_rim_inflows.columns].mean()
        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100
        print("Maximum differences:")
        print(df_diffs.sort_values(by='Max Difference', ascending=False).to_string())
        print('Creating comparison plots...')
        create_rim_inflow_comparison_plots(df_rim_inflows, df_reference)
