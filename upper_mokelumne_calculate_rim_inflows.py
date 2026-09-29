import pandas as pd

#from Examples.Example_SingleRimInflow_I_RCK001 import df_unimpaired_data
from extension_functions import *
from unimpairment_functions import *
from rim_inflow_functions import *
from evaporation_functions import *

if __name__ == "__main__":
    i_final_year = 2021
    print("done with imports")

    # --- Begin Flags ---
    # option to plot comparison
    b_compare_data = True

    # --- End Flags

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # file path and name must be provided to plot/calculate comparison and to use SV INPUTS from sheets as upstream
    # data
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.csv"
    s_prev_rim_inflow_sheet = "Inflows"

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Figures/Model_Comparison', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_mokelumne_full_gauge_data.csv', index_col=0, parse_dates=True)

    # ----------------------------------
    # --- GAP FILL AND DROP, ROUND 1 ---
    # ----------------------------------
    # in CMP001, fill the JNKSN_STORAGE in December 1965 with linear interpolation of the adjacent months.
    df_full_data.loc['1965-12-31', 'JNKSN_STORAGE'] = (df_full_data.loc['1965-11-30', 'JNKSN_STORAGE']
                                                       + df_full_data.loc['1966-01-31', 'JNKSN_STORAGE']) / 2
    # for JNKSN, create a copy of data with dropped WY1955
    df_full_data.rename(columns={'11332500': '11332500_v1'}, inplace=True)
    df_full_data["11332500_v2"] = df_full_data["11332500_v1"].copy()
    df_full_data.loc["1954-10-31":"1955-10-01", "11332500_v2"] = float("nan")
    # for CMP014, create a copy of data with dropped WY1955 and WY1956
    df_full_data.loc["1954-10-31":"1956-10-01", "11331500"] = float("nan")

    # -----------------------------
    # --- MERGE AND COPY GAUGES ---
    # -----------------------------

    # -- begin 11319500 merges --
    #### these two versions of 11319500 use different data sources (USGS vs EBMUD) and different gap filling. Neither one
    #### is obviously better at first glance.
    # with COL003 (11319500), EBMUD is main historical gage (pre-2021) but NaN's are filled with CDEC MKM
    # Later the filled out USGS 11319500 is used for s-curve on the COL003
    # gage, which is USGS 11315000. Version 1 is used for COL003
    if '11319500_v1' not in df_full_data.columns:
        df_full_data['11319500_v1'] = np.nan
    df_full_data['11319500_v1'] = df_full_data['EBMUD_11319500'].fillna(df_full_data['MKM'])

    # 11319500_v2 is created for use in MOK079. This is the USGS gage 11319500. Compare with COL003 above.
    if '11319500_v2' not in df_full_data.columns:
        df_full_data['11319500_v2'] = np.nan
    df_full_data['11319500_v2'] = df_full_data['11319500'].copy()
    # -- end 11319500 merges --

    # for JNKSN, create a copy of data with dropped WY1955. Sheet said "Do not use '55 as flow impacted by dam."
    df_full_data.rename(columns={'11332500': '11332500_v1'}, inplace=True)
    df_full_data["11332500_v2"] = df_full_data["11332500_v1"].copy()
    df_full_data.loc["1954-10-31":"1955-10-01", "11332500_v2"] = float("nan")

    # see DSC035. df_full_data['11327000_v2'] is created to drop part of the data for before extension. the rest of the
    # data from the main dataset (df_full_data['11327000'] is later copied over the extension data where available.
    df_full_data['11327000_v2'] = df_full_data['11327000'].copy()
    # fill before October 1960 with NaN.
    df_full_data.loc[:'1960-10-01', '11327000_v2'] = float("nan")

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_gap_filled.csv')

    # -------------------
    # --- EVAPORATION ---
    # -------------------

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_NHGAN(s_evap_dss_path, df_full_data)      # see NHGAN
    calc_evap_OHGAN(s_evap_dss_path, df_full_data)      # see NHGAN
    calc_evap_JNKSN(s_evap_dss_path, df_full_data)      # see CMP001

    df_full_data.to_csv('./Intermediate/upper_mokelumne_full_gauge_data_wevap.csv')

    # -----------------------------
    # --- UNIMPAIRMENT, ROUND 1 ---
    # -----------------------------

    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows, round 1 ...")

    # see the top of this doc for details on the lbear_ss errors.
    df_unimpaired_data['LBearSS'] = unimpaired_lbear_salt_springs_fnf(df_full_data)              # see SLTSP and UBEAR
    df_unimpaired_data['11309500'] = unimpaired_11309500_for_NHGAN(df_full_data)                        # see NHGAN
    df_unimpaired_data['NF_SF_ITAS'] = unimpaired_NF_SF_ITAS(df_full_data)                              # see NHGAN
    df_unimpaired_data['NH_DAM_RELEASE'] = unimpaired_NH_DAM_RELEASE(df_full_data)                      # see NHGAN
    df_unimpaired_data['11319500_v2'] = unimpaired_11319500_v2(df_full_data)                            # see MOK079
    df_unimpaired_data['11335000'] = unimpaired_11335000(df_full_data)                                  # see CMP001
    df_unimpaired_data['11333000'] = unimpaired_11333000(df_full_data)                                  # see CMP001


    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # ----------------------------------
    # --- GAP FILL AND DROP, ROUND 2 ---
    # ----------------------------------


    # see DEE023, 11335700 WY1967 is gap filled with WY1965 times a ratio of annual flows from 11335000
    d_65 = df_unimpaired_data.loc['1964-10-01':'1965-10-01', '11335000'].sum()     # annual flow for WY65
    d_67 = df_unimpaired_data.loc['1966-10-01':'1967-10-01', '11335000'].sum()     # annual flow for WY67
    df_shifted = df_full_data['11335700'].copy()
    # create a copy of the data shifted forward 2 years
    df_shifted.index = df_shifted.index + pd.DateOffset(years=2)
    # keep one copy of 11335700 unmodified
    df_full_data['11335700_v1'] = df_full_data['11335700'].copy()
    # modify the other copy
    df_full_data.loc['1966-10-01':'1967-10-01' , '11335700'] = (df_shifted.loc['1966-10-01':'1967-10-01']
                                                                * (d_67 / d_65))

    # ------------------------
    # --- S-CURVE, ROUND 1 ---
    # ------------------------

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    print("Extending flows, part 1...")
    # extend with the s-curve disaggregation, round 1
    extend_data(df_full_data['11317000'], df_full_data['11318500'],
                df_extended_data, df_synthetic_data, 1934, i_final_year, False,
                '11318500', i_final_year=i_final_year)                                              # see SFM005
    # for JNKSN, s-curve
    extend_data(df_unimpaired_data['11335000'], df_full_data['11332500_v2'],
                df_extended_data, df_synthetic_data, 1947, 1954, False,
                '11332500', i_final_year=i_final_year)                                               # see JNKSN
    extend_data(df_unimpaired_data['11335000'], df_unimpaired_data['11333000'],
                df_extended_data, df_synthetic_data, 1956, 2004, False,
                '11333000', i_final_year=i_final_year)                                               # see CMP001
    extend_data(df_unimpaired_data['11335000'], df_full_data['11331500'],
                df_extended_data, df_synthetic_data, 1949, 1954, False,
                '11331500', i_final_year=i_final_year)                                               # see CMP014
    extend_data(df_unimpaired_data['11335000'], df_full_data['11326300'],
                df_extended_data, df_synthetic_data, 1961, 1970, False,
                '11326300', i_final_year=i_final_year)                                               # see DSC035
    extend_data(df_unimpaired_data['11335000'], df_full_data['11327000_v2'],
                df_extended_data, df_synthetic_data, 1961, 1980, False,
                '11327000_v2', i_final_year=i_final_year)                                            # see DSC035
    extend_data(df_unimpaired_data['11335000'], df_full_data['11335700'],
                df_extended_data, df_synthetic_data, 1961, 1977, False,
                '11335700', i_final_year=i_final_year, s_strange_sheet='DEE023')                     # see DEE023

    # -----------------------------
    # --- UNIMPAIRMENT, ROUND 2 ---
    # -----------------------------

    # unimpairing the data for those that rely on previously s-curved data
    print("Calculating unimpaired flows, round 2...")
    df_unimpaired_data['11319500_v1'] = unimpaired_11319500(df_full_data, df_extended_data)                 # see COL003
    df_unimpaired_data['11316600'] = unimpaired_11316600(df_full_data, df_extended_data,
                                                         df_unimpaired_data)                                # see NFM010
    df_unimpaired_data['tiger_creek_conduit_accretions'] = unimpaired_tiger_creek_conduit_accretions(df_full_data,
                                                                df_extended_data)                           # see TGC003
    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_mokelumne_unimpaired_data.csv')

    # ------------------------
    # --- S-CURVE, ROUND 2 ---
    # ------------------------

    print("Extending flows, part 2...")

    extend_data_multi_model(df_unimpaired_data['11319500_v1'], df_full_data['11318500'], df_full_data['11317000'],
                            df_full_data['11318500'], df_extended_data, df_synthetic_data,
                            1934, 2021, 1934, 2021, False, '11318500',
                            "Model A", "Model B", i_x_start_year=1922,
                            i_final_year=2021, s_strange_sheet='')                                           # SFM005 A/B
    extend_data(df_unimpaired_data['11319500_v1'], df_full_data['11315000'],
               df_extended_data, df_synthetic_data, 1928, i_final_year, False,
               '11315000', i_x_start_year=1922, i_final_year=i_final_year, s_strange_sheet='COL003') # see COL003
    extend_data(df_unimpaired_data['11319500_v1'], df_unimpaired_data['LBearSS'],
               df_extended_data, df_synthetic_data, 1989, i_final_year, False,
               'LBearSS', i_final_year=i_final_year)                                              # see SLTSP and UBEAR
    extend_data(df_unimpaired_data['11319500_v1'], df_unimpaired_data['11316600'],
                df_extended_data, df_synthetic_data, 1986, i_y_end_year=2001,
                b_use_all_y_data=False, s_name='11316600', i_final_year=i_final_year)                       # see NFM010

    # -------------------------------
    # --- FILL DATA AFTER S-CURVE ---
    # -------------------------------

    # copy synthetic data to extended data where extended data is NaN for 11315000 and
    df_extended_data.fillna({'11315000': df_synthetic_data['11315000']}, inplace=True)                # see COL003
    df_extended_data.fillna({'11316600': df_synthetic_data['11316600']}, inplace=True)                # see NFM010

    # see DSC035. copy data from 11327000 onto 11327000 extended data for the dates Oct 1936 - Nov 1941
    df_extended_data.loc['1935-10-30':'1941-10-01', '11327000_v2'] = df_full_data.loc['1935-10-30':'1941-10-01', '11327000']

    # see DEE023. copy data in WY67 from 11335700 to 11335700_v1 after s-curve
    df_extended_data.loc['1966-10-01':'1967-10-01','11335700'] = df_full_data.loc['1966-10-01':'1967-10-01' , '11335700']
    # save to csv
    df_extended_data.to_csv('./Intermediate/upper_mokelumne_extended_data.csv')
    df_synthetic_data.to_csv('./Intermediate/upper_mokelumne_synthetic_data.csv')

    # -----------------------------
    # --- CALCULATE RIM INFLOWS ---
    # -----------------------------

    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    I_MFM008(df_full_data, df_rim_inflows)
    I_SFM005(df_extended_data, df_rim_inflows)
    I_COL003(df_extended_data, df_rim_inflows)
    I_SLTSP(df_extended_data['LBearSS'], df_extended_data['11315000'], df_rim_inflows)
    I_UBEAR(df_extended_data['LBearSS'], df_extended_data['11315000'], df_rim_inflows)
    I_NFM010(df_extended_data['11316600'], df_rim_inflows)
    I_TGC003(df_rim_inflows['I_NFM010'], df_rim_inflows)
    I_NHGAN(df_unimpaired_data[['11309500']], df_unimpaired_data[['NF_SF_ITAS']],
            df_unimpaired_data[['NH_DAM_RELEASE']], df_rim_inflows)
    I_PARDE(df_rim_inflows)
    I_CMCHE(df_rim_inflows)
    I_JNKSN(df_extended_data['11332500'], df_rim_inflows)
    I_CMP001(df_extended_data[['11333000']], df_rim_inflows[['I_JNKSN']], df_rim_inflows)
    I_CMP014(df_extended_data[['11333000']], df_rim_inflows[['I_JNKSN']], df_rim_inflows)
    I_CSM035(df_unimpaired_data[['11335000']], df_rim_inflows[['I_JNKSN']], df_rim_inflows[['I_CMP001']],
         df_rim_inflows[['I_CMP014']], df_rim_inflows)
    I_AMADR(df_unimpaired_data[['11335000']], df_rim_inflows)
    I_DSC035(df_extended_data[['11326300']], df_extended_data[['11327000_v2']], df_rim_inflows)
    I_DEE023(df_extended_data[['11335700']], df_rim_inflows)

    df_rim_inflows.to_csv('./Outputs/upper_mokelumne_rim_inflows.csv')

    # ----------------------------------------------
    # --- COMPARE TO PREVIOUS RIM INFLOW DATASET ---
    # ----------------------------------------------

    if b_compare_data:

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
            pct_vals = np.where(ref_vals != 0, np.abs(rim_vals - ref_vals) / ref_vals * 100, 0)

        df_diffs['Max Percent Difference'] = pct_vals
        # -------------------------------------------------------------------------------
        # calculate RMSE
        df_rmse = np.sqrt(((df_reference[df_rim_inflows.columns] - df_rim_inflows) ** 2).mean()).to_frame("RMSE")
        df_diffs = df_diffs.join(df_rmse)

        print("note the CMP014 will not show agreement in the following table because the python code is replicating the rev G version,")
        print("but the CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm file has the rev F version. In calculating CSM035, the inflows")
        print("from CMP014 are subtracted near the end of the calculation, causing knock-on effects.")

        # format output

        cols_to_format = ["Max Difference", "P50 Abs Diff", "P90 Abs Diff", "P95 Abs Diff", "P99 Abs Diff",
                          "Max Percent Difference", "RMSE"]

        df_diffs[cols_to_format] = df_diffs[cols_to_format].apply(
            lambda s: s.map(lambda v: f"{v:.6f}")
        )

        # space out column headers
        df_diffs.columns = [col + "   " for col in df_diffs.columns]

        # print the analysis table
        print(df_diffs.sort_values(by='Max Difference   ', ascending=False).to_string())

        print('Creating comparison plots...')

        # drop the first row of df rim inflows trimmed so it matches the reference
        df_rim_inflows.drop(index=df_rim_inflows.index[0], inplace=True)

        #trim our new inflows (from df_rim_inflows) to have the same number of rows as our reference
        i_targetLen=len(df_reference)
        df_rim_inflows_trimmed = df_rim_inflows.iloc[:i_targetLen].copy()

        create_rim_inflow_comparison_plots(df_rim_inflows_trimmed, df_reference)
