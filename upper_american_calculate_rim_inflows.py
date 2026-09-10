from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    # option to save s-curve parameters
    b_save_stats = True
    if b_save_stats and not os.path.exists('Outputs/SCurveStats.csv'): # if s-curve parameter output is desired and the output file doesn't exist, create initial output file to write to
        pd.DataFrame(columns=['reference location','target location','stat','value']).to_csv('Outputs/SCurveStats.csv',index=False)

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compareData = False
    s_prev_rim_inflows_fn = "CS3_Sac_ReadAllInflowDatatoDSS_05.18.23.xlsm" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_american_full_gauge_data.csv', index_col=0, parse_dates=True)

    # gap fill the data sets that need it
    gap_fill(df_full_data, {'11428300': list(range(2016,2022)), '11436950': [1922, 1923, 1924],
                            '11435900': [1922, 1923], '11434900': list(range(1929, 1933)),'11442000': [1922]},
             i_final_year)

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_american_full_gauge_data_gap_filled.csv')

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_11427400(s_evap_dss_path, df_full_data)
    calc_evap_11436950(s_evap_dss_path, df_full_data)
    calc_evap_11435900(s_evap_dss_path, df_full_data)
    calc_evap_11434900(s_evap_dss_path, df_full_data)
    calc_evap_11428700(s_evap_dss_path, df_full_data)
    calc_evap_11429350(s_evap_dss_path, df_full_data)
    calc_evap_11429600(s_evap_dss_path, df_full_data)
    calc_evap_EDN(s_evap_dss_path, df_full_data)
    calc_evap_11426170(s_evap_dss_path, df_full_data)
    calc_evap_11441000(s_evap_dss_path, df_full_data)
    calc_evap_11441100(s_evap_dss_path, df_full_data)
    # calc_evap_folsom(s_evap_dss_path, df_full_data)
    # calc_evap_NAT(s_evap_dss_path, df_full_data)


    df_full_data.to_csv('./Intermediate/upper_american_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows...")

    df_unimpaired_data['11439501'] = unimpaired_11439501(df_full_data)
    df_unimpaired_data['11427500'] = unimpaired_11427500(df_full_data)
    df_unimpaired_data['11427760'] = unimpaired_11427760(df_full_data)
    df_unimpaired_data['11428000'] = unimpaired_11428000(df_full_data)
    df_unimpaired_data['11428400'] = unimpaired_11428400(df_full_data)
    df_unimpaired_data['11428800'] = unimpaired_11428800(df_full_data)
    df_unimpaired_data['11429500'] = unimpaired_11429500(df_full_data)
    df_unimpaired_data['11430000'] = unimpaired_11430000(df_full_data)
    df_unimpaired_data['11433040'] = unimpaired_11433040(df_full_data)
    df_unimpaired_data['11433100'] = unimpaired_11433100(df_full_data)
    df_unimpaired_data['11433300'] = unimpaired_11433300(df_full_data)
    df_unimpaired_data['11433500'] = unimpaired_11433500(df_full_data)
    df_unimpaired_data['11435100'] = unimpaired_11435100(df_full_data)
    df_unimpaired_data['11437000'] = unimpaired_11437000(df_full_data)
    df_unimpaired_data['11436000'] = unimpaired_11436000(df_full_data)
    df_unimpaired_data['11426190'] = unimpaired_11426190(df_full_data)
    df_unimpaired_data['11427000'] = unimpaired_11427000(df_full_data)
    df_unimpaired_data['11426500'] = unimpaired_11426500(df_full_data)
    df_unimpaired_data['11441000'] = unimpaired_11441000(df_full_data)
    df_unimpaired_data['11441500'] = unimpaired_11441500(df_full_data)
    df_unimpaired_data['11443500'] = unimpaired_11443500(df_full_data)
    df_unimpaired_data['11444500'] = unimpaired_11444500(df_full_data)
    df_unimpaired_data['11444201'] = unimpaired_11444201(df_full_data)
    df_unimpaired_data['CalSim3'] = unimpaired_calsim3(df_full_data)

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_american_unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/upper_american_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows...")

    # extend all with the s-curve disaggregation
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11439501'], df_extended_data, df_synthetic_data, 1923, i_final_year, False, '11439501', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_full_data['11427700'], df_extended_data, df_synthetic_data, 1961, i_final_year, False, '11427700', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11427500'], df_extended_data, df_synthetic_data, 1966, 2007,True, '11427500', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11427760'], df_extended_data, df_synthetic_data, 1966, 2007, False, '11427760', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11428000'], df_extended_data, df_synthetic_data, 1957, 1986, False, '11428000', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11428400'], df_extended_data, df_synthetic_data, 1991, 2015, False, '11428400', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11428800'], df_extended_data, df_synthetic_data, 1966, 2007, True, '11428800', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11429500'], df_extended_data, df_synthetic_data, 1963, i_final_year, False, '11429500', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11430000'], df_extended_data, df_synthetic_data, 1963, 2021, False, '11430000', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11433040'], df_extended_data, df_synthetic_data, 1962, 2017, True, '11433040', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11433100'], df_extended_data, df_synthetic_data, 1967, 1992, False, '11433100', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11433100'], df_extended_data, df_synthetic_data, 1967, 1992, False, '11433100_AMF', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_full_data['11433260'], df_extended_data, df_synthetic_data, 1966, 1985, False, '11433260', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11433300'], df_extended_data, df_synthetic_data, 1959, i_final_year, False, '11433300', i_final_year=i_final_year,b_save_stats=b_save_stats)
    df_extended_data['11433500'] = flow_from_two_unimp(df_unimpaired_data['11433500'], df_unimpaired_data['11433300'], 1.06)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11435100'][~df_unimpaired_data.index.isin(pd.date_range(datetime(2002, 10, 31), datetime(2012, 9, 30)))], df_extended_data, df_synthetic_data, 1971, 2002, True, '11435100_C', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11435100'].loc[datetime(2011, 9, 30):], df_extended_data, df_synthetic_data, 2012, 2021, False, '11435100_A', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_unimpaired_data['11435100'].loc[datetime(2011, 9, 30):], df_extended_data, df_synthetic_data, 2012, 2021, False, '11435100_B', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11437000'], df_extended_data, df_synthetic_data, 1923, 1992, True, '11437000_A', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11437000'], df_extended_data, df_synthetic_data, 1923, 1992, False, '11437000_B', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_pos_unimpaired_data['11436000'], df_extended_data, df_synthetic_data, 1923, i_final_year, False, '11436000', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_full_data['11440000'], df_extended_data, df_synthetic_data, 1923, 1981, False, '11440000_A', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_full_data['11440000'], df_extended_data, df_synthetic_data, 1923, 1981, False, '11440000_B', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_full_data['11440500'], df_extended_data, df_synthetic_data, 1923, 1939, False, '11440500_A', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], df_full_data['11440500'], df_extended_data, df_synthetic_data, 1923, 1939, False, '11440500_B', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_extended_data['11439501'], monthly_to_timeseries(timeseries_to_monthly(df_unimpaired_data['11441000']).dropna(how='any', axis=0).drop(1962, axis=0))['TAF'], df_extended_data, df_synthetic_data, 1925, 1960, True, '11441000', i_final_year=i_final_year,b_save_stats=b_save_stats)
    # wy 1981 and 1994 use the synthetic values
    df_extended_data.loc[pd.date_range(datetime(1980, 10, 31), datetime(1981, 9, 30), freq='ME'), '11441000'] = df_synthetic_data.loc[pd.date_range(datetime(1980, 10, 31), datetime(1981, 9, 30), freq='ME'), '11441000'].values
    df_extended_data.loc[pd.date_range(datetime(1993, 10, 31), datetime(1994, 9, 30), freq='ME'), '11441000'] = df_synthetic_data.loc[pd.date_range(datetime(1993, 10, 31), datetime(1994, 9, 30), freq='ME'), '11441000'].values
    extend_data(df_full_data['11442000'], df_pos_unimpaired_data['11441500'], df_extended_data, df_synthetic_data, 1925, i_final_year, True, '11441500', i_final_year=1961,b_save_stats=b_save_stats)
    # wy 1962 and on are blank, fill with the original values
    df_extended_data.fillna({'11441500': df_pos_unimpaired_data['11441500']}, inplace=True)
    extend_data(df_extended_data['11439501'], df_full_data['11442000'], df_extended_data, df_synthetic_data, 1923, 1961, False, '11442000', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11443500'], df_extended_data, df_synthetic_data, 1974, 2021, True, '11443500_A', i_final_year=i_final_year,b_save_stats=b_save_stats)
    df_extended_data.loc[df_pos_unimpaired_data.loc[:datetime(2021,9,30), '11443500'].dropna().index, '11443500_A'] = df_pos_unimpaired_data.loc[:datetime(2021,9,30), '11443500'].dropna()
    extend_data(df_pos_unimpaired_data['11444500'], df_pos_unimpaired_data['11443500'], df_extended_data, df_synthetic_data, 1974, 2021, True, '11443500_D', i_x_start_year=1965, i_final_year=i_final_year,b_save_stats=b_save_stats)
    df_extended_data.fillna({'11443500_D': df_pos_unimpaired_data['11443500']}, inplace=True)
    extend_data(df_full_data['AMF'], df_unimpaired_data['11444201'], df_extended_data, df_synthetic_data, 1987, 2008, True, '11444201', i_final_year=i_final_year,b_save_stats=b_save_stats)
    # replace the end of wy 2017
    df_extended_data.loc[datetime(2016, 11, 30): datetime(2017, 9, 30), '11444201'] = df_unimpaired_data.loc[datetime(2016, 11, 30): datetime(2017, 9, 30), '11444201']
    extend_data(df_full_data['AMF'], df_pos_unimpaired_data['11444500'], df_extended_data, df_synthetic_data, 1965, i_final_year, False, '11444500', i_final_year=i_final_year,b_save_stats=b_save_stats)
    extend_data(df_full_data['AMF'], df_full_data['11446000'], df_extended_data, df_synthetic_data, 1944, 1959, False, '11446000', i_final_year=i_final_year,b_save_stats=b_save_stats)

    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_american_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_american_synthetic_data.csv')

    df_lake_valley_watershed = calculate_watershed_factors("./Inputs/lake_valley_watershed.csv")

    # final rim inflows
    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    I_DCC010(df_extended_data, df_rim_inflows)
    I_FRMDW(df_extended_data, df_rim_inflows)
    I_MFA036(df_extended_data, df_rim_inflows)
    I_RUB047(df_extended_data, df_rim_inflows)
    I_LRB004(df_extended_data, df_rim_inflows)
    I_HHOLE(df_extended_data, df_rim_inflows)
    I_LOONL(df_extended_data, df_rim_inflows)
    I_SFR006(df_extended_data, df_rim_inflows)
    I_GERLE(df_extended_data, df_rim_inflows)
    I_STMPY(df_extended_data, df_rim_inflows)
    I_PLC007(df_extended_data, df_rim_inflows)
    I_NLC003(df_extended_data, df_full_data, df_rim_inflows)
    I_SLC003(df_extended_data, df_full_data, df_rim_inflows)
    I_LNG012(df_extended_data, df_rim_inflows)
    I_RUB002(df_extended_data, df_rim_inflows)
    I_NMA003(df_extended_data, df_rim_inflows)
    I_MFA025(df_extended_data, df_rim_inflows)
    I_MFA023(df_extended_data, df_rim_inflows)
    I_MFA001(df_extended_data, df_rim_inflows)
    I_ALOHA(df_extended_data, df_rim_inflows)
    I_PYR001(df_extended_data, df_rim_inflows)
    I_CAPLS(df_extended_data, df_rim_inflows)
    I_SILVR(df_extended_data, df_rim_inflows)
    I_LKVLY(df_unimpaired_data, df_full_data, df_rim_inflows, df_lake_valley_watershed)
    I_NNA013(df_unimpaired_data, df_full_data, df_rim_inflows, df_lake_valley_watershed)
    I_NFA054(df_unimpaired_data, df_rim_inflows, df_lake_valley_watershed)
    I_CYN009(df_unimpaired_data, df_rim_inflows, df_lake_valley_watershed)
    I_NFA022(df_unimpaired_data, df_rim_inflows)
    I_NFA016(df_rim_inflows)
    I_SFA066(df_extended_data, df_rim_inflows)
    I_SFA076(df_rim_inflows)
    I_SLF009(df_rim_inflows)
    I_ALD004(df_extended_data, df_rim_inflows)
    I_ALD002(df_extended_data, df_rim_inflows)
    I_PLM001(df_extended_data, df_rim_inflows)
    I_UNVLY(df_extended_data, df_rim_inflows)
    I_ICEHS(df_extended_data, df_rim_inflows)
    I_SLV006(df_extended_data, df_rim_inflows)
    I_SLV015(df_extended_data, df_rim_inflows)
    I_BSH003(df_extended_data, df_rim_inflows)
    I_SFA040(df_extended_data, df_rim_inflows)
    I_RCK001(df_extended_data, df_rim_inflows)
    I_SFA030(df_extended_data, df_rim_inflows)
    I_WBR001(df_extended_data, df_rim_inflows)
    I_FOLSM(df_full_data, df_unimpaired_data, df_rim_inflows)
    I_ECHOL(df_extended_data, df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_american_rim_inflows.csv')

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
