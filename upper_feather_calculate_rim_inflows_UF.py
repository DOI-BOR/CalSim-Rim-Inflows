from extension_functions import *
from unimpairment_functions_UF import *
from rim_inflow_functions_UF import *
from evaporation_functions_UF import *

if __name__ == "__main__":
    i_final_year = 2021

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compareData = True
    s_prev_rim_inflows_fn = "CS3_Sac_ReadAllInflowDatatoDSS_05.18.23.xlsm" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_feather_full_gauge_data.csv', index_col=0, parse_dates=True)

    # gap fill the data sets that need it
    #gap_fill(df_full_data, {'11428300': list(range(2016,2022)), '11436950': [1922, 1923, 1924],
    #                        '11435900': [1922, 1923], '11434900': list(range(1929, 1933)),'11442000': [1922]},
    #         i_final_year)

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_feather_full_gauge_data_gap_filled.csv')

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
   
    calc_evap_FRD(s_evap_dss_path, df_full_data)
    calc_evap_DAV(s_evap_dss_path, df_full_data)
    calc_evap_11404250(s_evap_dss_path, df_full_data)
    calc_evap_11399000(s_evap_dss_path, df_full_data)
    calc_evap_MMW(s_evap_dss_path, df_full_data)
    calc_evap_BTV(s_evap_dss_path, df_full_data)
    calc_evap_ANT(s_evap_dss_path, df_full_data)
    calc_evap_11403500(s_evap_dss_path, df_full_data)
    calc_evap_11403520(s_evap_dss_path, df_full_data)
    calc_evap_11395020(s_evap_dss_path, df_full_data)
    calc_evap_11395400(s_evap_dss_path, df_full_data)
    calc_evap_RVPHB(s_evap_dss_path, df_full_data)
    # calc_evap_folsom(s_evap_dss_path, df_full_data)
    # calc_evap_NAT(s_evap_dss_path, df_full_data)


    df_full_data.to_csv('./Intermediate/upper_feather_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows...")

    df_unimpaired_data['11391400'] = unimpaired_11391400(df_full_data)
    df_unimpaired_data['11404300'] = unimpaired_11404300(df_full_data)
    df_unimpaired_data['11399500'] = unimpaired_11399500(df_full_data)
    df_unimpaired_data['11401112'] = unimpaired_11401112(df_full_data)
    df_unimpaired_data['11400500'] = unimpaired_11400500(df_full_data)
    df_unimpaired_data['11400000'] = unimpaired_11400000(df_full_data)
    df_unimpaired_data['11401500'] = unimpaired_11401500(df_full_data)
    df_unimpaired_data['11401125'] = unimpaired_11401125(df_full_data) 
    df_unimpaired_data['11403000'] = unimpaired_11403000(df_full_data)
    df_unimpaired_data['11403530'] = unimpaired_11403530(df_full_data)
    df_unimpaired_data['11394500'] = unimpaired_11394500(df_full_data)
    df_unimpaired_data['11394500_A'] = unimpaired_11394500_A(df_full_data)
    df_unimpaired_data['11391500'] = unimpaired_11391500(df_full_data)
    df_unimpaired_data['11392100'] = unimpaired_11392100(df_full_data)
    df_unimpaired_data['11406500'] = unimpaired_11406500(df_full_data)
    df_unimpaired_data['11403200'] = unimpaired_11403200(df_full_data)
    df_unimpaired_data['11404500'] = unimpaired_11404500(df_full_data)
    df_unimpaired_data['11395030'] = unimpaired_11395030(df_full_data)
    df_unimpaired_data['11396000'] = unimpaired_11396000(df_full_data)
    df_unimpaired_data['11395200'] = unimpaired_11395200(df_full_data)
    df_unimpaired_data['11397000'] = unimpaired_11397000(df_full_data)
    df_unimpaired_data['Unimpaired_ORO'] = unimpaired_ORO(df_full_data)
    

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_feather_unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/upper_feather_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows...")

    # extend all with the s-curve disaggregation
    extend_data(df_full_data['FTO'], df_unimpaired_data['11404300'], df_extended_data, df_synthetic_data, 1994, i_final_year, False, '11404300', i_final_year=i_final_year)
    FTO_A = df_full_data['FTO'].copy()
    #FTO_A.loc[datetime(2018,10,31):datetime(2019,9,30)]= None
    FTO_A.loc[datetime(1936,10,31):datetime(1964,9,30)]= None
    df_11400500 = df_unimpaired_data['11400500']
    df_11400500.loc[datetime(2018,10,31):datetime(2019,9,30)]= None
    df_11400500.loc[datetime(1936,10,31):datetime(1964,9,30)]= None
    extend_data(FTO_A, df_11400500, df_extended_data, df_synthetic_data, 1965, 2018, False, '11400500', i_final_year=i_final_year)
    
    df_11399500 = df_full_data['FPR'].copy()  
    df_11401112 = df_unimpaired_data['11401112'].copy()
    df_11399500[datetime(1992,10,31):datetime(2021,9,30)] = df_unimpaired_data['11399500'][datetime(1992,10,31):datetime(2021,9,30)]
    df_11399500[datetime(2016,10,31):datetime(2019,9,30)] = None
    df_11401112[datetime(2016,10,31):datetime(2019,9,30)] = None
    extend_data(df_11399500,df_11401112 , df_extended_data, df_synthetic_data, 1981, 2016, False, '11401112', i_final_year=i_final_year)
    extend_data(df_unimpaired_data['11401500'], df_unimpaired_data['11401125'], df_extended_data, df_synthetic_data, 1966, 1980, False, '11401125', i_final_year=1993)
    extend_data(df_full_data['FTO'],df_full_data['ANT_FNF'], df_extended_data, df_synthetic_data, 1964, 2021, False, 'ANT_FNF', i_final_year=i_final_year)
    extend_data(df_full_data['FTO'],df_unimpaired_data["11403530"], df_extended_data, df_synthetic_data, 1999, 2021, False, '11403530', i_final_year=i_final_year)        
    extend_data(df_full_data['FTO'],df_unimpaired_data["11403000"], df_extended_data, df_synthetic_data, 1951, 1961, False, '11403000', i_final_year=i_final_year)
    df_11394500 =df_full_data['FTM'].copy()+df_full_data['LLCID_DIV'].copy()
    df_11394500[datetime(1952,10,31):datetime(2021,9,30)]=df_unimpaired_data['11394500'][datetime(1952,10,31):datetime(2021,9,30)]   
    extend_data(df_11394500 ,df_unimpaired_data["11391500"], df_extended_data, df_synthetic_data, 1969, 1980, False, '11391500', i_final_year=i_final_year)
    df_FRD_FNF=df_full_data['FRD_FNF'].copy()
    extend_data(df_11394500 ,df_full_data["FRD_FNF"], df_extended_data, df_synthetic_data, 1966, 2021, False, '11391400', i_final_year=i_final_year)
    extend_data(df_full_data['FTO'] ,df_unimpaired_data["11406500"], df_extended_data, df_synthetic_data, 1931, 1963, False, '11406500', i_final_year=i_final_year)
    df_11404500=df_unimpaired_data['11404500'].copy()
    df_11404500[datetime(1921,10,31):datetime(1966,9,30)]=df_full_data['FPL'][datetime(1921,10,31):datetime(1966,9,30)]+0.2*df_full_data['FTO_CU'][datetime(1921,10,31):datetime(1966,9,30)]
    extend_data(df_11404500, df_unimpaired_data["11403200"], df_extended_data, df_synthetic_data, 1987, 2021, False, '11403200', i_final_year=i_final_year)    
    extend_datav2(df_full_data['FTO'], df_pos_unimpaired_data['11395030'],  df_extended_data, df_synthetic_data, 1964, 2016, True, '11395030',  i_final_year=i_final_year, exclude_from_regression=list(range(1928, 1934)) + [2017]) #note range(start, end) = start to (end-1)
    extend_datav2(df_full_data['FTO'], df_pos_unimpaired_data['11396000'],  df_extended_data, df_synthetic_data, 1974, 2021, True, '11396000',  i_final_year=i_final_year, exclude_from_regression=list([1973, 2012]))
    extend_datav2(df_full_data['FTO'], df_pos_unimpaired_data['11395200'],  df_extended_data, df_synthetic_data, 1973, 2021, False, '11395200',  i_final_year=i_final_year)
    extend_datav2(df_full_data['FTO'], df_pos_unimpaired_data['11397000'],  df_extended_data, df_synthetic_data, 1922, 1987, True, '11397000',  i_final_year=i_final_year)
    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_feather_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_feather_synthetic_data.csv')

    df_lake_valley_watershed = calculate_watershed_factors("./Inputs/lake_valley_watershed.csv")

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

  
    I_GZL009(df_extended_data, df_rim_inflows)
    I_ALMNR(df_unimpaired_data, df_full_data, df_rim_inflows)
    I_MTMDW(df_unimpaired_data, df_full_data, df_rim_inflows)
    I_BTVLY(df_extended_data,df_unimpaired_data, df_rim_inflows)
    I_NFF058(df_extended_data,df_unimpaired_data, df_rim_inflows)
    I_ANTLP(df_extended_data, df_rim_inflows)
    I_EBF001(df_extended_data,df_unimpaired_data, df_rim_inflows)
    I_NFF046(df_extended_data,df_rim_inflows)
    I_UBUCK(df_extended_data, df_rim_inflows)
    I_LBUCK(df_extended_data, df_rim_inflows)
    I_MLK003(df_extended_data, df_rim_inflows)
    I_NFF029(df_unimpaired_data, df_full_data, df_rim_inflows)
    I_DAVIS(df_extended_data,df_unimpaired_data, df_full_data, df_rim_inflows)
    I_FRMAN(df_extended_data,df_full_data, df_rim_inflows)
    I_MFF087(df_unimpaired_data, df_full_data, df_rim_inflows)
    I_MFF019(df_unimpaired_data, df_full_data, df_rim_inflows)
    I_WBF006(df_extended_data, df_rim_inflows)
    I_WBF015(df_extended_data, df_rim_inflows)
    I_WBF030(df_extended_data, df_rim_inflows)
    I_RVPHB(df_extended_data, df_rim_inflows)
    I_LGRSV(df_extended_data, df_rim_inflows)
    I_SLYCK(df_extended_data, df_rim_inflows, df_synthetic_data)
    I_LSTCK(df_rim_inflows)
    I_SFF029(df_extended_data, df_rim_inflows)
    I_SFF019(df_extended_data, df_rim_inflows)
    I_SFF011(df_extended_data, df_rim_inflows)
    I_OROVL(df_full_data, df_unimpaired_data, df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_feather_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compareData:

        # read in data
        df_reference = pd.read_excel(s_prev_rim_inflows_fn, sheet_name=s_prev_rim_inflow_sheet, skiprows=[0,2,3,4,5,6,7,8,9,10,11],header=0, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')
        df_diffs['Median Value - Original'] = df_reference[df_rim_inflows.columns].mean()
        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100

        print("Maximum differences:")
        print(df_diffs.sort_values(by='Max Difference', ascending=False).to_string())

        print('Creating comparison plots...')
        create_rim_inflow_comparison_plots(df_rim_inflows, df_reference)
