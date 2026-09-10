import pandas as pd

# ----------------------------------------------
# ---                INPUTS                  ---
# ----------------------------------------------

# Rim Inflow Basins (Names must match RimInflow Output files)
sl_rim_inflow_basins = ["upper_american","upper_mokelumne"]

# Summary Period
i_final_year = 2021
i_start_year = 1921

# ----------------------------------------------
# --- FORMAT & OUTPUT S-CURVE SUMMARY TABLE  ---
# ----------------------------------------------

# read in s_curve ouptut file
s_scurveStats_fn = 'Outputs/SCurveStats.csv'
df_scurve = pd.read_csv(s_scurveStats_fn)

# remove the fit_slope and fit_intercept (these are duplicates, currently calculated in two functions of the rim inflow workflow, these values are exactly the same)
df_scurve = df_scurve[[not(s_stat in ['fit_slope','fit_intercept']) for s_stat in df_scurve.stat]]

# pivot the table
df_scurve.drop_duplicates(inplace=True)
df_scurve_format = df_scurve.pivot(index = ['reference location','target location'],columns='stat',values='value')
df_scurve_format = df_scurve_format[['slope','intercept','r2']].reset_index()

# To Do - add gage/lodation names, will require input table to cross reference gage #s and Names

# save the output
df_scurve_format.round(3).to_csv('Outputs/RimInflows_Summary_SCurveParameters.csv',index=False)

# ----------------------------------------------
# ---  CALCULATE & OUTPUT RIM INFLOW SUMMARY TABLE    ---
# ----------------------------------------------

# read in final rim inflow output csv files from each basin and merge into a single dataframe 
dl_basins = [pd.read_csv(f'Outputs/{s}_rim_inflows.csv',index_col=0) for s in sl_rim_inflow_basins]
df_rim_inflows = pd.concat(dl_basins,axis=1)
df_rim_inflows.index = pd.to_datetime(df_rim_inflows.index)

# clip to selected period
# Question why does I_AMADR go to 2024-08-31??
# Question why does the upper_mokelumne_rim_inflows.csv have a 1921-09-30
df_rim_inflows = df_rim_inflows[df_rim_inflows.index < pd.to_datetime(str(i_final_year) + '-10-01')]
df_rim_inflows = df_rim_inflows[df_rim_inflows.index > pd.to_datetime(str(i_start_year) + '-09-30')]

# calculate mean and median monthly values for each rim inflow
df_rim_inflows_monthlyTS = df_rim_inflows.resample('ME').sum()
df_rim_inflows_meanMon = df_rim_inflows_monthlyTS.groupby(df_rim_inflows_monthlyTS.index.month_name()).mean().T 
df_rim_inflows_medianMon = df_rim_inflows_monthlyTS.groupby(df_rim_inflows_monthlyTS.index.month_name()).median().T

# calculate mean and median total annual flow for each rim infow (calculated over water years)
df_rim_inflows['wy'] = df_rim_inflows.index.year.where(df_rim_inflows.index.month<10,df_rim_inflows.index.year+1)
df_rim_inflows_annualTS = df_rim_inflows.groupby('wy').sum()
df_rim_inflows_annualMetric = df_rim_inflows_annualTS.agg(["mean","median"]).T

# join monthly and annual datasets
df_rim_inflows_summaryMedian = pd.concat([df_rim_inflows_medianMon[['October','November','December','January','February','March','April','May','June','July','August','September']],
                            df_rim_inflows_annualMetric],axis=1)
df_rim_inflows_summaryMean = pd.concat([df_rim_inflows_meanMon[['October','November','December','January','February','March','April','May','June','July','August','September']],
                            df_rim_inflows_annualMetric],axis=1)

# output combined dataframes
df_rim_inflows_summaryMedian.to_csv('Outputs/RimInflows_Summary_MonthlyMedianandAnnualFlows.csv')
df_rim_inflows_summaryMean.to_csv('Outputs/RimInflows_Summary_MonthlyAvgandAnnualFlows.csv')

# ouptut combined dataframes rounded to one decimal place for the final tables
df_rim_inflows_summaryMedian.round(1).to_csv('Outputs/RimInflows_Summary_MonthlyMedianandAnnualFlows_rounded.csv')
df_rim_inflows_summaryMean.round(1).to_csv('Outputs/RimInflows_Summary_MonthlyAvgandAnnualFlows_rounded.csv')
