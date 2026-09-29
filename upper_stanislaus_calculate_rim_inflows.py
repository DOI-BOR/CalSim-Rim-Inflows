from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021

    # flag to output additional information to console
    b_verbose = False

    # this reproduces various errors or issues found in the workbooks
    b_reproduce_errors = True
        # error 1: in LYONS,should be identical to MODELA tab in SFS030 BUT, even though it says "Run then replace Feb-
        # Sep 1940 with historical data" the 2022F version of the sheet does not have the data replaced with historical data.
        # error 2: Spicer Meadows Evaporation rate is from CS3_ER_SPICE_REV1.xlsm rather than the most recent evap rate,
        # _except_ in SPICE, where it uses the current evap rate.

    # this isolates the s-curve from the rest of the calculation by reading in the sheet inputs and outputs to the
    # s-curve and using the output value to move forward in the calculation.
    b_replicate_sheets = True

    # this keeps all the data in the MODELA s-curve in DONLL sheet. The sheet discards data after 2011.
    b_donll_all_data = False

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # option to plot comparison
    b_compareData = True

    # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.csv" # file path and name must be provided to plot/calculate comparison
    s_prev_rim_inflow_sheet = "Inflows"

    if b_reproduce_errors:
        # use this to check the code after the s-curve. The Excel s-curve suffers from the bug that arises when water
        # years end with negative values.
        df_nfs009_post_s_curve = pd.read_csv('./Inputs/s_curve_replication/nfs009_output_from_s_curve.csv')

    if b_replicate_sheets:
        # read in files that contain the sheet data from just before and just after the s-curve process, to isolate that
        # factor. The "after s" files are the data from the sheets after merging the synthetic output into the gaps in
        # the data.

        # create a list of lists. inner elements are ['column_name', 'path to before csv', 'path to after csv']
        ls_sheet_info = [['NFS009', './Inputs/s_curve_replication/nfs009_input_to_s_curve.csv',
                          './Inputs/s_curve_replication/nfs009_output_from_s_curve.csv'],
                         ]
        # create the dataframes where we keep the before and after data
        df_before_s = pd.DataFrame()
        df_after_s = pd.DataFrame()

        read_replication_data(ls_sheet_info, df_before_s, df_after_s)

        # read in the rim inflows from 20 sheets that are used in STS072
        df_inflows_for_sts072 = pd.read_csv('./inputs/upper_stanislaus_2022_extra_data_for_replication.csv', index_col=0, parse_dates=True)
    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_stanislaus_full_gauge_data.csv', index_col=0, parse_dates=True)

    if b_replicate_sheets:
        # merge the rim inflow data for STS072 into df_full_data
        df_full_data = pd.concat([df_full_data, df_inflows_for_sts072], axis=1)

    # read in the rim inflow from upper mokelumne (mokelumne/consumnes) for NHGAN
    df_temp = pd.read_csv('./Outputs/upper_mokelumne_rim_inflows.csv')
    df_temp = df_temp.set_index(df_temp.columns[0])
    df_temp.index = pd.to_datetime(df_temp.index)
    df_full_data['I_NHGAN'] = df_temp['I_NHGAN'].copy()

    # gap fill the data sets that need it
    gap_fill_11291000(df_full_data, i_final_year, b_reproduce_errors)                                       # see RLIEF
    df_full_data.loc['1957-02-01':'1957-09-30', '11292600'] =  \
        df_full_data.loc['1957-02-01':'1957-09-30', '11292600_COMP_MODEL']                                  # see DONLL
    df_full_data.loc['2006-10-01':'2007-09-30', '11292600'] =  \
        df_full_data.loc['2006-10-01':'2007-09-30', 'DON']                                                  # see DONLL
    if b_reproduce_errors:
        # see DONLL, tab "Donnell Storage"
        df_full_data.loc['1957-11-30':'1958-08-31', '11292600'] = df_full_data.loc['1957-11-30':'1958-08-31', '11292600'].apply(lambda v: round_half_up(v, 1))
        df_full_data.loc['2008-04-30':'2009-12-31', '11292600'] = df_full_data.loc['2008-04-30':'2009-12-31', '11292600'].apply(lambda v: round_half_up(v, 1))
        df_full_data.loc['1964-01-31', '11292600'] = 17.633
        df_full_data.loc['2006-09-30', '11292600'] = round_half_up(df_full_data.loc['2006-09-30', 'DON'], 1)
    if b_reproduce_errors:
        # round Donnell Storage from Oct 2006 to Aug 2015 to the nearest 0.1, always rounding up at 0.05  to match excel.
        df_full_data.loc['2006-10-01':'2015-08-31', '11292600'] = df_full_data.loc['2006-10-01':'2015-08-31', '11292600'].apply(lambda v: round_half_up(v, 1))
    # fill Beardsley storage gap with CDEC
    df_full_data.loc['2006-10-01':'2007-09-30', '11292800'] = df_full_data.loc['2006-10-01':'2007-09-30', 'BRD'] #see BEARD

    # fill gap in 11292860 using 11292901 minus 11292900, see BEARD
    df_full_data.loc['1986-05-01':'1986-09-30', '11292860'] = (
        df_full_data.loc['1986-05-01':'1986-09-30', '11292901']
        - df_full_data.loc['1986-05-01':'1986-09-30', '11292900'])
    # fill gap in 11292860 using 11292820 minus 11292900, see BEARD, from 10/31/2020 to 9/30/i_final_year
    df_full_data.loc['2020-10-01':str(i_final_year)+'-09-30', '11292860'] = (
        df_full_data.loc['2020-10-01':str(i_final_year)+'-09-30', '11292820'] -
        df_full_data.loc['2020-10-01':str(i_final_year)+'-09-30', '11292900'])

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_stanislaus_full_gauge_data_gap_filled.csv')

    # fill gages with monthly averages
    df_full_data['11295900_filled'] = fill_monthly_storage(df_full_data[['11295900']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=True, b_round=True)            # see PCRST and SFS033
    df_full_data['11297700_filled'] = fill_monthly_storage(df_full_data[['11297700']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=True, b_round=False)            # see LYONS
    df_full_data['11293460_filled'] = fill_monthly_storage(df_full_data[['11293460']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=False, b_round=True)           # see NFS033
    df_full_data['11293350_filled'] = fill_monthly_storage_w_middle_gap(df_full_data[['11293350']], 1980,
            10, 2006, 9, 2010, 10, i_final_year, 9, False , b_round=True)  # see NFS033
    df_full_data['11293370_filled'] = fill_monthly_storage(df_full_data[['11293370']], i_start_year=1980, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=False, b_round=True)            # see NFS033
    df_full_data['11297000_filled'] = fill_monthly_storage(df_full_data[['11297000']], i_start_year=1939, i_start_month=10,
                                i_end_year=i_final_year, i_end_month=9, b_first_month_zero=False, b_round=False)            # see BEARD
    # set pre-1930 Lyons Storage (1129770_filled) to zero, see LYONS
    df_full_data.loc[df_full_data.index < pd.Timestamp("1930-01-01"), '11297700_filled'] = 0

    # set Spicer Meadow storage before Feb 1989 to (filled) Alpine Storage times a factor. See NFS033 and SPICE
    df_full_data['11293770_filled'] = np.nan
    df_full_data.loc[df_full_data.index < pd.Timestamp("1989-02-28"), '11293770_filled'] =  \
        df_full_data.loc[df_full_data.index < pd.Timestamp("1989-02-28"), '11293460_filled'] * (4062/4231)
    # set Spicer Meadow storage after (and including) Feb 1989 to its own data. See NFS033
    df_full_data.loc[df_full_data.index >= pd.Timestamp("1989-02-28"), '11293770_filled'] =  \
        df_full_data.loc[df_full_data.index >= pd.Timestamp("1989-02-28"), '11293770']



    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_11295900(s_evap_dss_path, df_full_data)                                                   # see SFS033
    calc_evap_11297700(s_evap_dss_path, df_full_data)                                                   # see SFS030
    calc_evap_11293460(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293350(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293370(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    calc_evap_11293770(s_evap_dss_path, df_full_data, b_reproduce_errors)                               # see NFS033
    # evaps below (v2) are here to reproduce the correct evaps for SPICE (using up-to-date spicer meadow evap rate) when using
    # the old evap rate for other sheets. If b_reproduce_errors = False, these should be the same as the evaps above
    calc_evap_11293770_v2(s_evap_dss_path, df_full_data)                                               # see SPICE
    calc_evap_11293460_v2(s_evap_dss_path, df_full_data)                                               # see SPICE
    calc_evap_11293350_v2(s_evap_dss_path, df_full_data)                                               # see SPICE
    calc_evap_11293370_v2(s_evap_dss_path, df_full_data)                                               # see SPICE

    calc_evap_11291000(s_evap_dss_path, df_full_data, b_replicate_sheets)                              # see RLIEF
    calc_evap_11292600(s_evap_dss_path, df_full_data, b_replicate_sheets)                              # see DONLL
    calc_evap_11292800(s_evap_dss_path, df_full_data)                                                  # see BEARD
    if b_reproduce_errors:
        calc_evap_11291000_v2(s_evap_dss_path, df_full_data, b_replicate_sheets)                       # see BEARD

    df_full_data.to_csv('./Intermediate/upper_stanislaus_full_gauge_data_wevap.csv')

    ### unimpairing the data
    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows...")

    df_unimpaired_data['11296500'] = unimpaired_11296500(df_full_data)                                  # see SFS033
    df_unimpaired_data['11298000'] = unimpaired_11298000(df_full_data)                                  # see SFS030
    df_unimpaired_data['11293600'] = unimpaired_11293600(df_full_data)                                  # see NFS033
    df_unimpaired_data['11294500'] = unimpaired_11294500(df_full_data, b_reproduce_errors)              # see NFS033
    df_unimpaired_data['11294000'] = unimpaired_11294000(df_full_data, b_reproduce_errors)              # see SPICE
    if b_reproduce_errors:
        df_unimpaired_data['11294500_v2'] = unimpaired_11294500_v2(df_full_data)                        # see SPICE
    df_unimpaired_data['11295210'] = df_full_data['11295210'] + df_full_data['11295230']                # see BVC007
    df_unimpaired_data['11292000'] = unimpaired_11292000(df_full_data, b_replicate_sheets)              # see RLIEF
    df_unimpaired_data['11292700'] = unimpaired_11292700(df_full_data, b_replicate_sheets)              # see DONLL
    df_unimpaired_data['11292900'] = unimpaired_11292900(df_full_data, b_replicate_sheets, b_reproduce_errors) # see BEARD
    df_unimpaired_data['11293000'] =  unimpaired_11293000(df_full_data, b_replicate_sheets, b_reproduce_errors) # see BEARD
    # merge two unimpaired gauges. see BEARD, sheet MF Stanislaus UNIMP
    df_unimpaired_data['mf_stanislaus'] = df_unimpaired_data['11293000'].fillna(df_unimpaired_data['11292900'] * 1.028)
    df_unimpaired_data['goodwin_fnf'] = unimpaired_goodwin_fnf(df_full_data, b_reproduce_errors)          # see STS072

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_stanislaus_unimpaired_data.csv')

    # redistribute negatives
    df_pos_unimpaired_data = remove_negatives_timeseries(df_unimpaired_data)

    # save to csv
    df_pos_unimpaired_data.to_csv('./Intermediate/upper_stanislaus_unimpaired_data_pos.csv')

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows...")

    # extend all with the s-curve disaggregation
    extend_data(df_full_data['SNS'], df_unimpaired_data['11296500'],
                df_extended_data, df_synthetic_data, 1939, i_final_year, False,
                '11296500', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see SFS033
    extend_data(df_full_data['SNS'], df_unimpaired_data['11298000'],
                df_extended_data, df_synthetic_data, 1941, i_final_year, False,
                '11298000', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see SFS030
    if b_reproduce_errors:
        df_extended_data['11298000_v2'] = df_extended_data['11298000']
    df_extended_data.loc['02-28-1940':'09-30-1940', '11298000'] = (
                df_unimpaired_data.loc)['02-28-1940':'09-30-1940', '11298000']                          # see SFS030

    if b_reproduce_errors:
        extend_data(df_full_data['SNS'], df_unimpaired_data['11294500_v2'],
                    df_extended_data, df_synthetic_data, 1929, i_final_year, False,
                    '11294500_v2', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see SPICE
        # replace extended data in 11294500 from WY 1922-1925 with observed data. See SPICE
        df_extended_data.loc[:'09-30-1925', '11294500_v2'] = df_unimpaired_data.loc[:'09-30-1925', '11294500_v2']  # see SPICE

    extend_data(df_full_data['SNS'], df_unimpaired_data['11294500'],
                df_extended_data, df_synthetic_data, 1929, i_final_year, False,
                '11294500', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS033
    # replace extended data in 11294500 from WY 1922-1925 with observed data. See NFS033
    df_extended_data.loc[:'09-30-1925', '11294500'] = (df_unimpaired_data.loc)[:'09-30-1925', '11294500'] # see NFS033

    extend_data(df_extended_data['11294500'], df_unimpaired_data['11293600'],
                df_extended_data, df_synthetic_data, 1953, i_final_year, False,
                '11293600', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS033
    if b_reproduce_errors:
        # use the 4500_v2 to NOT replicate errors in this s-curve by using the updated spicer meadows evap rate. SPICE
        extend_data(df_extended_data['11294500_v2'], df_unimpaired_data['11294000'],
                df_extended_data, df_synthetic_data, 1953, 1988, False,
                '11294000_v2', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='SPICE')  # see SPICE
    else:
        extend_data(df_extended_data['11294500'], df_unimpaired_data['11294000'],
                df_extended_data, df_synthetic_data, 1953, 1988, False,
                '11294000', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')     # see SPICE
    # if replicating errors, replace 1989-2020 with historical data, otherwise replace 1989-i_final_year with
    # historical data. See SPICE MODELC tab.
    if b_reproduce_errors:
        s_end_hist_fill = "2020-09-30"
        bf_mask = (df_extended_data.index >= "1988-10-01") & (df_extended_data.index <= s_end_hist_fill)
        df_extended_data.loc[bf_mask, '11294000_v2'] = df_unimpaired_data.loc[df_extended_data.index[bf_mask], '11294000']
    else:
        s_end_hist_fill = str(i_final_year) + "-09-30"
        bf_mask = (df_extended_data.index >= "1988-10-01") & (df_extended_data.index <= s_end_hist_fill)
        df_extended_data.loc[bf_mask, '11294000'] = df_unimpaired_data.loc[df_extended_data.index[bf_mask], '11294000']
    extend_data(df_full_data['SNS'], df_unimpaired_data['11295210'],
                df_extended_data, df_synthetic_data, 1991, i_final_year, False,
                '11295210', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')     # see BVC007
    extend_data(df_full_data['SNS'], df_unimpaired_data['11292000'],
                df_extended_data, df_synthetic_data, 1947, i_final_year, False,
                '11292000', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')      # see RLIEF
    df_extended_data.loc['1938-10-31':'1945-09-30', '11292000'] = (
                df_unimpaired_data.loc)['1938-10-31':'1945-09-30', '11292000']                              # see RLIEF
    extend_data(df_full_data['SNS'], df_full_data['11292500'],
                df_extended_data, df_synthetic_data, 1951, 1994, False,
                '11292500', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')     # see CFS001
    extend_data(df_full_data['SNS'], df_unimpaired_data.loc['1981-10-01':str(i_final_year)+'-09-30','mf_stanislaus'],
                df_extended_data, df_synthetic_data, 1982, i_final_year, False,
                '11293000', i_x_start_year=1922, i_final_year=i_final_year)     # see BEARD

    if b_donll_all_data:
        # see DONLL, improvement without discarding data
        extend_data(df_full_data['SNS'], df_unimpaired_data['11292700'],
                    df_extended_data, df_synthetic_data, 1973, 2010, True,
                    '11292700', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='DONLL')
    else:
        extend_data(df_full_data['SNS'], df_unimpaired_data['11292700'],
                    df_extended_data, df_synthetic_data, 1973, 2010, False,
                    '11292700', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see DONLL
        df_extended_data.loc['2011-10-01':'2015-09-30', '11292700'] = (
            df_unimpaired_data.loc)['2011-10-01':'2015-09-30', '11292700']  # see DONLL
        df_extended_data.loc['2016-10-01': str(i_final_year) + '-09-30', '11292700'] = (
            df_unimpaired_data.loc)['2016-10-01': str(i_final_year) + '-09-30', '11292700']  # see DONLL

    # BVC007 rim inflow must be calculated early because it is part of an unimpairment step in NFS009 before the s-curve
    # (extend_data) in that sheet.
    df_rim_inflows = pd.DataFrame()
    I_BVC007(df_extended_data[['11295210']], df_rim_inflows)
    df_unimpaired_data['11295300'] = unimpaired_11295300(df_full_data, df_rim_inflows, df_unimpaired_data, b_reproduce_errors)  # see NFS009
    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_stanislaus_unimpaired_data_part_2.csv')

    if b_reproduce_errors:
        extend_data(df_extended_data['11294500_v2'], df_unimpaired_data['11295300'],
                df_extended_data, df_synthetic_data, 1991, i_final_year, False,
                '11295300', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS009
    else:
        extend_data(df_extended_data['11294500'], df_unimpaired_data['11295300'],
                df_extended_data, df_synthetic_data, 1991, i_final_year, False,
                '11295300', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='')  # see NFS009


    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_stanislaus_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_stanislaus_synthetic_data.csv')

    # final rim inflows

    print("Calculating rim inflows...")

    I_SFS033(df_extended_data[['11296500']], df_rim_inflows)
    I_PCRST(df_extended_data[['11296500']], df_rim_inflows)
    I_SFS030(df_extended_data[['11298000']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']], df_rim_inflows)
    I_NFS033(df_extended_data[['11293600']], df_rim_inflows)
    I_MIL003(df_rim_inflows[['I_BVC007']], df_rim_inflows)
    I_ANG017(df_rim_inflows[['I_BVC007']], df_rim_inflows)
    I_RLIEF(df_extended_data[['11292000']], df_rim_inflows)
    I_MFS047(df_extended_data[['11292000']], df_rim_inflows)
    I_CFS001(df_extended_data[['11292500']], df_rim_inflows)
    I_DONLL(df_extended_data[['11292700']], df_rim_inflows[['I_RLIEF']], df_rim_inflows[['I_MFS047']],
                df_rim_inflows[['I_CFS001']], df_rim_inflows)
    I_MFS022(df_extended_data[['11292700']], df_rim_inflows[['I_RLIEF']], df_rim_inflows[['I_MFS047']],
                df_rim_inflows[['I_CFS001']], df_rim_inflows)
    if b_reproduce_errors:
        I_LYONS(df_extended_data[['11298000_v2']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']],
                df_rim_inflows[['I_SFS030']], df_rim_inflows)
        I_SPICE(df_extended_data[['11294000_v2']], df_rim_inflows)
    else:
        I_LYONS(df_extended_data[['11298000']], df_rim_inflows[['I_SFS033']], df_rim_inflows[['I_PCRST']],
            df_rim_inflows[['I_SFS030']], df_rim_inflows)
        I_SPICE(df_extended_data[['11294000']], df_rim_inflows)
    if b_replicate_sheets:
        I_NFS009(df_after_s[['NFS009']], df_rim_inflows)
        I_NFS005(df_after_s[['NFS009']], df_rim_inflows)
    else:
        I_NFS009(df_extended_data[['11295300']], df_rim_inflows)
        I_NFS005(df_extended_data[['11295300']], df_rim_inflows)
    I_BEARD(df_extended_data[['11293000']], df_rim_inflows[['I_RLIEF']], df_rim_inflows[['I_MFS047']],
                df_rim_inflows[['I_CFS001']], df_rim_inflows[['I_DONLL']], df_rim_inflows[['I_MFS022']], df_rim_inflows)
    I_MFS013(df_extended_data[['11293000']], df_rim_inflows[['I_RLIEF']], df_rim_inflows[['I_MFS047']],
                df_rim_inflows[['I_CFS001']], df_rim_inflows[['I_DONLL']], df_rim_inflows[['I_MFS022']], df_rim_inflows)
    I_TULOC(df_full_data[['I_NHGAN']], df_rim_inflows)
    I_STS059(df_full_data[['I_NHGAN']], df_rim_inflows)
    if b_replicate_sheets:
        I_STS072_v2(df_unimpaired_data[['goodwin_fnf']], df_rim_inflows, df_full_data)
    else:
        I_STS072(df_unimpaired_data[['goodwin_fnf']], df_rim_inflows)
    df_rim_inflows.to_csv('./Outputs/upper_stanislaus_rim_inflows.csv')

    # Comparison with Previous Rim Inflow dataset
    if b_compareData:
        if b_verbose:
            # Notes on replication
            print("The NFS033 and SPICE replications differ from Excel workbooks in two months, Aug and Sept 1924, due to ")
            print("an s-curve bug in Excel with negative flows at the end of the year. These two sheets ")
            print("use the same x watershed for s-curving.")

        # read in data
        df_reference = pd.read_csv(s_prev_rim_inflows_fn, index_col=0, parse_dates=True)

        # calculate differences
        df_diffs = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows).max().to_frame('Max Difference')

        # calculate percentile errors: the value of error that X% of the data is better than.
        # 1) Absolute differences per column
        diff_abs = (df_reference[df_rim_inflows.columns] - df_rim_inflows).abs()

        # 2) Choose percentiles you want (expressed as proportions)
        percentiles = [0.50, 0.90, 0.95, 0.99]

        # 3) Compute percentiles per column and give nice column names
        q_abs = diff_abs.quantile(percentiles).T
        q_abs.columns = [f'P{int(p * 100)} Abs Diff' for p in percentiles]

        # 4) Combine with your existing "Max Difference" table
        df_diffs = diff_abs.max().to_frame('Max Difference').join(q_abs)

        df_diffs.head()

        # Add the datetime where the max occurs per column
        df_diff = abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)
        df_diffs['Date of Max Difference'] = df_diff.idxmax()

        # --- Max Percent Difference computed at the max-diff timestamp per column ---
        # Prepare matrices for fast, aligned lookup
        df_ref_cols = df_reference[df_rim_inflows.columns]
        df_rim_cols = df_rim_inflows[df_rim_inflows.columns]

        # Map each column to the integer row index of its "Date of Max Difference"
        row_idx = df_ref_cols.index.get_indexer(df_diffs['Date of Max Difference'])
        col_idx = np.arange(len(df_rim_inflows.columns))

        # Extract values from each column at its own max-diff row
        ref_vals = df_ref_cols.to_numpy()[row_idx, col_idx]
        rim_vals = df_rim_cols.to_numpy()[row_idx, col_idx]

        # Percent difference: |rim - ref| / ref * 100 (guard against divide-by-zero)
        with np.errstate(divide='ignore', invalid='ignore'):
            pct_vals = np.where(ref_vals != 0, np.abs(rim_vals - ref_vals) / ref_vals * 100, np.nan)

        df_diffs['Max Percent Difference'] = pct_vals
        # -------------------------------------------------------------------------------

        # calculate RMSE
        df_rmse = np.sqrt(((df_reference[df_rim_inflows.columns] - df_rim_inflows) ** 2).mean()).to_frame("RMSE")
        df_diffs = df_diffs.join(df_rmse)

        # calculate RMSE divided by average value of inflow
        df_rmse_over_avg = (df_rmse['RMSE']/df_rim_inflows.mean()).to_frame('RMSE over Avg')
        df_diffs = df_diffs.join(df_rmse_over_avg)

        # format output
        cols_to_format = ["Max Difference", "P50 Abs Diff", "P90 Abs Diff", "P95 Abs Diff", "P99 Abs Diff",
                          "Max Percent Difference", "RMSE", "RMSE over Avg"]

        df_diffs[cols_to_format] = df_diffs[cols_to_format].apply(
            lambda s: s.map(lambda v: f"{v:.6f}")
        )

        # space out column headers
        df_diffs.columns = [col + "   " for col in df_diffs.columns]

        # print the analysis table
        print(df_diffs.sort_values(by='Max Difference   ', ascending=False).to_string())

        print('Creating comparison plots...')

        # Drop the first row of df_rim_inflows if its index month is September (month == 9) to match df_reference
        if df_rim_inflows.index[0].month == 9:
            df_rim_inflows = df_rim_inflows.iloc[1:]

        #trim our new inflows (from df_rim_inflows) to have the same number of rows as our reference
        i_targetLen=len(df_reference)
        df_rim_inflows_trimmed = df_rim_inflows.iloc[:i_targetLen].copy()

        create_rim_inflow_comparison_plots(df_rim_inflows_trimmed, df_reference)