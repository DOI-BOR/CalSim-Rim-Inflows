from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    ti_storage_range = pd.date_range("1921-09-30", f"{i_final_year}-09-30", freq="ME")
    ti_calculate_range = pd.date_range("1921-10-31", f"{i_final_year}-09-30", freq="ME")

    # this holds the already extended evap rates
    s_evap_dss_path = r"./Inputs/evaporation_rates.dss"

    # option to plot comparison
    b_compareData = True
    s_prev_rim_inflows_fn = "CS3_FthYub_ReadAllInflowDatatoDSS_05.18.23.csv" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/feather_yuba_full_gauge_data.csv', index_col=0, parse_dates=True)

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_JKSMD(s_evap_dss_path, df_full_data)
    # two versions of evap data calculation: the NFY029 seems to use shorter table than JKSMD sheet
    calc_evap_JKSMD_I_NFY029(s_evap_dss_path, df_full_data)
    calc_evap_BOWMN(s_evap_dss_path, df_full_data)
    calc_evap_FRNCH(s_evap_dss_path, df_full_data)
    calc_evap_FRDYC(s_evap_dss_path, df_full_data)
    calc_evap_RLLNS(s_evap_dss_path, df_full_data)
    calc_evap_CMBIE(s_evap_dss_path, df_full_data)
    calc_evap_CMPFW(s_evap_dss_path, df_full_data)
    # there is two version of the storage data, but they give same values, so maybe we don't need it
    calc_evap_RLLNS(s_evap_dss_path, df_full_data, s_data_suffix="_I_RLLNS")
    calc_evap_CMBIE(s_evap_dss_path, df_full_data, s_data_suffix="_I_RLLNS")
    calc_evap_CMPFW(s_evap_dss_path, df_full_data, s_data_suffix="_I_RLLNS")
    calc_evap_MERLC(s_evap_dss_path, df_full_data)
    calc_evap_SPLDG(s_evap_dss_path, df_full_data)

    df_full_data.to_csv('./Intermediate/feather_yuba_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame(index=ti_storage_range)

    print("Calculating unimpaired flows...")

    df_unimpaired_data['11409000'] = unimpaired_11409000(df_full_data)
    df_unimpaired_data['11409400'] = unimpaired_11409400(df_full_data)
    df_unimpaired_data['11422500'] = unimpaired_11422500(df_full_data)
    df_unimpaired_data['11424000'] = unimpaired_11424000(df_full_data)
    df_unimpaired_data['11414100'] = unimpaired_11414100(df_full_data)
    df_unimpaired_data['MERLC'] = unimpaired_MERLC(df_full_data)
    df_unimpaired_data['11390000'] = df_full_data['11390000'] - df_full_data['11389800']
    df_unimpaired_data['11414250'] = unimpaired_11414250(df_full_data)
    df_unimpaired_data['FERC'] = unimpaired_FERC()
    df_unimpaired_data['11417500'] = unimpaired_11417500(df_full_data)

    # drop the first row used for storage
    df_unimpaired_data = df_unimpaired_data.loc[ti_calculate_range,:]

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/feather_yuba_unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/feather_yuba_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame(index=ti_storage_range)
    df_synthetic_data = pd.DataFrame(index=ti_storage_range)

    print("Extending flows...")
    # extend some with the s-curve disaggregation
    extend_data(df_unimpaired_data['11409000'], df_full_data['11413000'], df_extended_data, df_synthetic_data, 1939, 2021, False, '11413000', i_x_start_year=1922, i_final_year=1968)
    extend_data(df_full_data.loc[:, "11409300"], df_unimpaired_data['11409400'], df_extended_data, df_synthetic_data, 1969, 1995, False, '11409400', i_x_start_year=1968, i_final_year=2000)
    #  this has NA when it should not....

    ## BUG TODO
    ### setting these values to NA is necessary; I thought the 1965 in the function arg 
    ### is supposed to understand the range it's supposed to read from....
    ### relevant code in s_curve_disaggregation below:
    ## dl_y_month_avgs = [0] + df_y_data.loc[i_y_start_year:i_y_end_year, :].mean(axis=0).tolist()
    df_unimpaired_copy = df_unimpaired_data['11422500'].copy(deep=True)
    df_unimpaired_copy.loc[:"1964-09"] = pd.NA
    extend_data(df_unimpaired_data.loc[:, "11424000"], df_unimpaired_copy, df_extended_data, df_synthetic_data, 1965, i_final_year, False, '11422500', s_strange_sheet="RLLNS")

    # this depends on the extension after the first round of unimpaired calculation
    df_unimpaired_data['11409400_EXT'] = unimpaired_11409400_ext(df_full_data, df_extended_data, df_unimpaired_data)
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)
    
    # final rim inflows
    df_rim_inflows = pd.DataFrame(index=ti_storage_range)
    
    print("Calculating rim inflows...")
    # This is input to other nodes so we need it before others
    I_NFY029(df_extended_data, df_full_data, df_unimpaired_data, df_rim_inflows)
    I_OGN005(df_pos_unimpaired_data, df_rim_inflows)
    # doesn't seem to depend on NFY029 even if it's in excel sheet
    I_RLLNS(df_extended_data, df_unimpaired_data, df_rim_inflows)
    
    # extend some with the s-curve disaggregation that depend on rim inflows
    extend_data(df_rim_inflows["I_NFY029"], df_full_data.loc[:, "WILSON_CREEK"], df_extended_data, df_synthetic_data, 1976, 2004, False, 'WILSON_CREEK', i_x_start_year=1922, i_final_year=i_final_year)
    extend_data(df_unimpaired_data['11390000'], df_pos_unimpaired_data['MERLC'], df_extended_data, df_synthetic_data, 1968, 1980, False, 'MERLC_MODELA', i_final_year=i_final_year)
    extend_data(df_rim_inflows["I_OGN005"], df_pos_unimpaired_data['MERLC'], df_extended_data, df_synthetic_data, 1968, 1980, False, 'MERLC_MODELB', i_final_year=i_final_year, s_strange_sheet="MERLC_MODELB")

    
    # these two unimpaired depend on WILSON CREEK
    df_unimpaired_data['11416500'] = unimpaired_11416500(df_full_data, df_extended_data).loc[ti_calculate_range]
    df_unimpaired_data['11408550'] = unimpaired_11408550(df_full_data, df_extended_data).loc[ti_calculate_range]
    # 7900 requires data from 8550
    df_unimpaired_data['11407900'] = unimpaired_11407900(df_full_data, df_unimpaired_data)
    # 11424000 acrretion requires RLLNS
    df_unimpaired_data["11424000_ACC"] = unimpaired_11424000_ACC(df_full_data, df_rim_inflows)
    df_unimpaired_data['11408880'] = unimpaired_11408880(df_full_data, df_extended_data)
    # I_MFY013 calculates it in a different manner
    df_unimpaired_data['11409000_I_MFY013'] = unimpaired_11409000_I_MFY013(df_full_data, df_extended_data)
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)
    
    extend_data(df_rim_inflows["I_NFY029"], df_pos_unimpaired_data["11416500"], df_extended_data, df_synthetic_data, 1928, i_final_year, False, '11416500', i_x_start_year=1922, i_final_year=i_final_year)
    
    extend_data(df_rim_inflows["I_NFY029"], df_unimpaired_data["11407900"], df_extended_data, df_synthetic_data, 1936, i_final_year, False, '11407900', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet="JKSMD")
    extend_data(df_rim_inflows.loc[:, "I_NFY029"], df_unimpaired_data['11417500'], df_extended_data, df_synthetic_data, 1960, i_final_year, False, '11417500', i_x_start_year=1922, i_final_year=2021)

    # needed for MERLC_MODELA
    df_pos_extended_data = remove_negatives_timeseries(df_extended_data)
    # # save to csv
    df_extended_data.to_csv('./Intermediate/feather_yuba_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/feather_yuba_synthetic_data.csv')

    # this function also calculates I_FRNCH
    I_BOWMN(df_extended_data, df_rim_inflows)
    I_JKSMD(df_extended_data, df_unimpaired_data, df_rim_inflows)
    I_CMBIE(df_pos_unimpaired_data, df_rim_inflows)
    I_MERLC(df_extended_data, df_pos_extended_data, df_rim_inflows)
    
    # these extension depend on BOWMAN so
    # three models to extend this station
    extend_data(df_full_data.loc[:, "11414000"], df_pos_unimpaired_data['11414100'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414100', i_x_start_year=1943, i_final_year=1994)
    extend_data(df_rim_inflows.loc[:, "I_NFY029"], df_pos_unimpaired_data['11414100'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414100_NFY029', i_x_start_year=1922, i_final_year=2021)
    extend_data(df_rim_inflows.loc[:, "I_BOWMN"], df_pos_unimpaired_data['11414100'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414100_BOWMN', i_x_start_year=1928, i_final_year=2021)
    extend_data(df_rim_inflows.loc[:, "I_NFY029"], df_full_data['11414000'], df_extended_data, df_synthetic_data, 1943, i_final_year, False, '11414000_NFY029', i_x_start_year=1922, i_final_year=2021)
    extend_data(df_rim_inflows.loc[:, "I_BOWMN"], df_full_data['11414000'], df_extended_data, df_synthetic_data, 1943, i_final_year, False, '11414000_BOWMN', i_x_start_year=1928, i_final_year=2021)
    extend_data(df_rim_inflows.loc[:, "I_NFY029"], df_unimpaired_data['11414250'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414250_NFY029', i_x_start_year=1922, i_final_year=2021)
    extend_data(df_rim_inflows.loc[:, "I_BOWMN"], df_unimpaired_data['11414250'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414250_BOWMN', i_x_start_year=1928, i_final_year=2021, s_strange_sheet="SPLDG_MODELC")
    extend_data(df_full_data["11414000"], df_unimpaired_data['11414250'], df_extended_data, df_synthetic_data, 1967, i_final_year, False, '11414250_MODELD', i_x_start_year=1943, i_final_year=1994)

    extend_data(df_rim_inflows.loc[:, "I_NFY029"], df_unimpaired_data['FERC'], df_extended_data, df_synthetic_data, 1976, 2008, False, 'FERC_NFY029', i_x_start_year=1922, i_final_year=i_final_year)
    extend_data(df_rim_inflows.loc[:, "I_BOWMN"], df_unimpaired_data['FERC'], df_extended_data, df_synthetic_data, 1976, 2008, False, 'FERC_BOWMN', i_x_start_year=1928, i_final_year=i_final_year)
    extend_data(df_full_data["11414000"], df_unimpaired_data['FERC'], df_extended_data, df_synthetic_data, 1976, 2008, False, 'FERC_11414000', i_x_start_year=1943, i_final_year=i_final_year)
    extend_data(df_full_data["11414000"], df_unimpaired_data['FERC'], df_extended_data, df_synthetic_data, 1976, 2008, False, 'FERC_11414000_2', i_x_start_year=1943, i_final_year=1994)

    I_FRDYC(df_extended_data, df_pos_unimpaired_data, df_rim_inflows)
    I_MFY013(df_extended_data, df_pos_unimpaired_data, df_rim_inflows)
    I_SFY048(df_extended_data, df_full_data, df_rim_inflows)
    I_SPLDG(df_extended_data, df_unimpaired_data, df_rim_inflows)
    I_LCBRF(df_extended_data, df_unimpaired_data, df_rim_inflows)

    I_SFY007(df_extended_data, df_rim_inflows)
    # We have one extra date at the beginning for storage
    df_rim_inflows = df_rim_inflows.loc[ti_calculate_range]
    df_rim_inflows.to_csv('./Outputs/feather_yuba_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compareData:

        # read in data
        df_reference = pd.read_csv(s_prev_rim_inflows_fn, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')
        df_diffs['Na Values'] = df_rim_inflows.isna().sum()
        df_diffs['Median Value - Original'] = df_reference[df_rim_inflows.columns].mean()
        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100

        print("Maximum differences:")
        print(df_diffs.sort_values(by='Max Difference', ascending=False).to_string())

        print('Creating comparison plots...')

        create_rim_inflow_comparison_plots(df_rim_inflows, df_reference)
