import rim_inflow_functions
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

    # option to run each element using "upstream" (antecedent) SV INPUT values from sheets rather than from the values
    # calculated within the Python code.
    b_use_upstream_sv_inputs = True

    # This flag initiates two things: 1) a check to see that the upstream code up until we reach the inputs for the s-curve
    # disaggregation match the excel workbooks. It checks the x watershed and y watershed against data in files that end
    # in "input_to_s_curve.csv".  2) It takes the s-curve from the sheets (found in files that end in
    # "output_from_s_curve.csv") and runs the code downstream of that point. It compares the final output to the
    # SV INPUT tab of the sheets (found in "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm").
    b_replicate_sheets = True

    # --- End Flags

    # this holds the already extended evap rates
    s_evap_dss_path = r".\Inputs\evaporation_rates.dss"

    # file path and name must be provided to plot/calculate comparison and to use SV INPUTS from sheets as upstream
    # data
    s_prev_rim_inflows_fn = "CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.csv"
    s_prev_rim_inflow_sheet = "Inflows"

    # path for some extra sv inputs
    s_prev_rim_inflows_extra = r".\Inputs\upper_tuolumne_2022_sv_inputs.csv"
    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)
    os.makedirs('./Figures', exist_ok=True)
    os.makedirs('./Figures/Model_Comparison', exist_ok=True)
    os.makedirs('./Outputs', exist_ok=True)

    # read in the data that we already read in
    df_full_data = pd.read_csv('./Intermediate/upper_tuolumne_full_gauge_data.csv', index_col=0, parse_dates=True)

    # read in upper mokelumne rim inflows, I_NHGAN needed for DCM027
    df_mokelumne_rim_inflows = pd.read_csv('./Outputs/upper_mokelumne_rim_inflows.csv', index_col=0, parse_dates=True)


    # ----------------------------------
    # ---     GAP FILL AND DROP      ---
    # ----------------------------------

    # TO DO - update the gap_fill_similarWYs to allow for only either NAs or specified time periods.

    # 11267350 in the I_MCLRE spreadsheet 
    # 1978 - 1987 are gapfilled with 'similar year types'
    df_full_data['11267350_og'] = df_full_data['11267350'].values # save the original dataset
    gap_fill_similarWYs([(1978,1996),(1979,2000),(1980,2005),(1981,1989),(1982,2005),(1983,1995),(1984,2000),(1985,2001),
        (1986,2005),(1987,1994)],df_full_data,'11267350')
    df_full_data.loc['1987-04':'1987-09','11267350'] = df_full_data.loc['1987-04':'1987-09','11267350_og'].values # these values we don't want to replace with similar water years

    # 11242350 - multiple gapfilling methods - from the I_BUR005 spreadheet
    df_full_data.loc['1977-07':'1977-09','11242350'] = 0     # 7/31/1977, 8/31/1977, and 9/30/1977 are gapfilled with zeros..
    df_full_data.loc['1990-10':'1990-12','11242350'] = df_full_data.loc['1991-10':'1991-12','11242350'].values     # 10/31/1990 is filled with 10/31/1991, 11/30/1990 filled with 11/30/1991, and 12/31/1990 filled with 12/31/1991
    # Longer gaps filled based on water years
    df_full_data['11242350_og'] = df_full_data['11242350'].values # save the original dataset
    gap_fill_similarWYs([(1981,1992),(1982,2005),(1983,1995),(1984,1999),(1985,1991),(1986,2005),(1987,1994),(1988,1992),
        (1989,1992),(1990,1992),(2000,1999),(2001,1991),(2002,1991),(2003,2009)], df_full_data,'11242350')
    df_full_data.loc['1999-10':'1999-12','11242350'] = df_full_data.loc['1999-10':'1999-12','11242350_og'].values # keep original values
    df_full_data.loc['2003-01':'2003-09','11242350'] = df_full_data.loc['2003-01':'2003-09','11242350_og'].values # keep original values
    
    # CDEC TLG, gapfilled with a zeron on 9/30/2020
    df_full_data.loc["2020-09",'TLG'] = 0

    # -----------------------------
    # --- MERGE AND COPY GAUGES ---
    # -----------------------------

    # save to csv
    df_full_data.to_csv('./Intermediate/upper_tuolumne_full_gauge_data_gap_filled.csv')

    # -------------------
    # --- EVAPORATION ---
    # -------------------

    print("Calculating evaporation...")

    # calculate the evaporation amounts for all of our reservoirs
    calc_evap_MCLRE(s_evap_dss_path, df_full_data)      # see MCLRE
    calc_evap_ESTMN(s_evap_dss_path,df_full_data)         # see ESTMN

    df_full_data.to_csv('./Intermediate/upper_tuolumne_full_gauge_data_wevap.csv')

    # -----------------------------
    # --- UNIMPAIRMENT, ROUND 1 ---
    # -----------------------------

    df_unimpaired_data = pd.DataFrame()

    print("Calculating unimpaired flows ....")

    df_unimpaired_data['11270000'] = unimpaired_11270000(df_full_data) # from I_MCLRE
    df_unimpaired_data['11257500'] = unimpaired_11257500(df_full_data) # from I_BUR005
    df_unimpaired_data['11257500_ESTMN'] = unimpaired_11257500(df_full_data.copy().drop(columns='11267350').rename(columns={'11267350_ESTMN':'11267350'})) # from I_ESTMN TO DO remove with initial round of improements. 
    df_unimpaired_data['11259000'] = unimpaired_11259000(df_full_data) # from I_ESTMN 
    df_unimpaired_data['ESTMNOutflow'] = unimpaired_ESTMNOutflow(df_full_data) # from I_ESTMN

    # drop the first row which is only for calculating storage differences
    df_unimpaired_data.drop(index=df_unimpaired_data.index[0], inplace=True)

    # save to csv
    df_unimpaired_data.to_csv('./Intermediate/upper_tuolumne_unimpaired_data.csv')

    # ------------------------
    # --- S-CURVE, ROUND 1 ---
    # ------------------------

    df_extended_data = pd.DataFrame()
    df_synthetic_data = pd.DataFrame()

    # -- Burns Reservoir Outflow - Extended with Unimpaired USGS 11257500 Data, from I_BUR005 spreadsheet
    extend_data(df_unimpaired_data['11257500'], df_full_data['BurnsReservoirOutflow'],
            df_extended_data, df_synthetic_data, 1950, 2021, False,
            'BurnsReservoirOutflow', i_x_start_year=1922, i_final_year=1990)                     
    df_extended_data = pd.concat([df_extended_data,df_full_data.loc['1990-10':f'{i_final_year}-09','BurnsReservoirOutflow']]) # TO DO, modify extend data function to keep the original y data for selected period?? 
    
    # extenion of 11271320 Dry Creek Near Snelling, CA is depending on I_NHGAN (inflow to hogan reservoir)
    extend_data(df_mokelumne_rim_inflows['I_NHGAN'],df_full_data['11271320'], df_extended_data,df_synthetic_data,
            1967,1992,False,'11271320',i_x_start_year=1922,i_final_year=2021)                 # see DCM027

    # HTCHY MODEL A for extending SFPUC Inflow to Hetch Hetchy Reservoir uses Merced at Happy Isles Bridge, Model B Uses CDEC TLG
    extend_data_multi_model(df_full_data['11264500'],df_full_data['SFPUCHH'],
            df_full_data['TLG'],df_full_data['SFPUCHH'],df_extended_data,df_synthetic_data,1922,2015,1922,2015,b_use_all_y_data=True,
            s_name = 'SFPUCHH_',s_model_name_1='ModelA',s_model_name_2='ModelB',i_x_start_year=1922,i_final_year=i_final_year)
    df_extended_data['SFPUCHH'] =  df_extended_data['SFPUCHH_ModelB'] # Model B is selected over Model A for the final rim inflows.

    # -- Inflows to Lake Eleanor - Extended using CDEC TLG data
    extend_data(df_full_data['TLG'],df_full_data['SFPUCLE'],df_extended_data,df_synthetic_data,1922,2015,
        True,'SFPUCLE',1922,i_final_year=i_final_year)

    # -- Inflows to Lake Lloyd - Extended using CDEC TLG data
    extend_data(df_full_data['TLG'],df_full_data['SFPUCLL'],df_extended_data,df_synthetic_data,1922,2015,
        True,'SFPUCLL',1922,i_final_year=i_final_year)

    # -- Chowchilla R. Below Buchanan Dam near Raymond - Extended using USGS Unimp Fresno R. Near Knowles, see I_ESTMN TODO replace w/ '11257500
    extend_data(df_unimpaired_data['11257500_ESTMN'],df_unimpaired_data['11259000'],df_extended_data,df_synthetic_data,
        1931,1990,True,'11259000',1922,1980)

    # -----------------------------
    # --- CALCULATE RIM INFLOWS ---
    # -----------------------------

    df_rim_inflows = pd.DataFrame()

    print("Calculating rim inflows...")

    I_MCLRE(df_full_data['MRC'],df_unimpaired_data['11270000'],df_rim_inflows)
    I_BUR005(df_extended_data['BurnsReservoirOutflow'],df_rim_inflows)
    I_MCD055(df_rim_inflows)
    I_DCM027(df_extended_data['11271320'],df_rim_inflows)
    I_HTCHY(df_extended_data['SFPUCHH'],df_rim_inflows)
    I_ELENR(df_extended_data['SFPUCLE'],df_rim_inflows)
    I_LLOYD(df_extended_data['SFPUCLL'],df_rim_inflows)
    I_ESTMN(df_extended_data['11259000'],df_unimpaired_data['ESTMNOutflow'], df_rim_inflows)
    I_TUO054(df_rim_inflows)
    I_PEDRO(df_full_data[['SFPUCLG','TLG']],df_rim_inflows)
    
    df_rim_inflows.to_csv('./Outputs/upper_tuolumne_rim_inflows.csv')

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

        df_diffs['Max Percent Difference'] = (abs(df_reference[df_rim_inflows.columns] - df_rim_inflows)).max() / df_reference[df_rim_inflows.columns].mean()*100
        # calculate RMSE
        df_rmse = np.sqrt(((df_reference[df_rim_inflows.columns] - df_rim_inflows) ** 2).mean()).to_frame("RMSE")
        df_diffs = df_diffs.join(df_rmse)

        print("note the CMP014 will not show agreement in the following table because the python code is replicating the rev G version,")
        print("but the CS3_SJR_ReadAllInflowDatatoDSS_05.17.23.xlsm file has the rev F version.")

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
