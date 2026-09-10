import numpy as np
import pandas as pd
import io, time
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from dataretrieval import waterdata
import ssl, certifi
import urllib.error, urllib.request
import os


def s_curve_disaggregation(df_x_data, df_y_data, i_x_start_year, i_x_end_year, i_y_start_year,
                           i_y_end_year, b_use_all_y=False, s_strange_sheet='',b_save_stats=False,
                           s_reference_name = '',s_target_name = '',s_out_stats = 'Outputs/SCurveStats.csv'):
    """
    Takes in the x data and the y data and generated a full timeseries of synthetic y data.
    This is meant to replicate what the Excel/VBA does for the S-Curve disaggregation.
    Parameters
    ----------
    df_x_data: series
        Full timeseries of x data. This is the reference unimpaired flow data. A pandas series.
    df_y_data: series
        Full timeseries of available y data. This is the data that is availiable for the location we want data for. A
        pandas series.
    i_x_start_year: int
        Start year of x data to use
    i_x_end_year: int
        End year of x data to use
    i_y_start_year: int
        Start year of y data to use
    i_y_end_year: int
        End year of y data to use
    b_use_all_y: bool
        Whether to use all y data or just the section in the Y years
    s_strange_sheet: string
        For a few sheets with strange modifications to the s-curve procedure, this is the sheet name with capital letters.
    b_save_stats: boolean
        Option to save s-curve stats
    s_reference_name: str
        Name of reference location, only needed if saving s_curve stats to file, i.e. b_save_stats = True
    s_target_name: str
        Name of target location, only needed if saving s_curve stats to file, i.e. b_save_stats = True
    s_out_stats: string
        Output file to save s-curve stats if b_save_stats is true

    Returns
    -------
    df_y_data_output: dataframe
        Full timeseries of y data. Y data in the selected rang is kept, the rest is synthetic.
    df_y_data_synthetic: dataframe
        Full timeseries of synthetic y data.
    """
    # if it is a series, get it into the monthly format
    if isinstance(df_x_data, pd.Series):
        df_x_data = timeseries_to_monthly(df_x_data.to_frame('TAF'))
        df_y_data = timeseries_to_monthly(df_y_data.to_frame('TAF'))

    # drop any missing data in either frame
    df_x_data.dropna(inplace=True)
    df_y_data.dropna(inplace=True)

    # trim the x data to just the specified years
    df_x_data = df_x_data.loc[i_x_start_year:i_x_end_year, :]

    # trim the y data to only the x years incase the y is longer for some reason
    df_y_data = df_y_data.loc[i_x_start_year:i_x_end_year, :]

    # first we want the x value monthly average for just the years of y data we want to keep
    # if working on COL003 (11315000), we need to use only 1944 to 2021 for monthly averages
    if (s_strange_sheet == 'COL003'):
        dl_x_month_avgs = [0] + df_x_data.loc[1944:i_y_end_year, :].mean(axis=0).tolist()
    else:
        dl_x_month_avgs = [0] + df_x_data.loc[i_y_start_year:i_y_end_year, :].mean(axis=0).tolist()

    # get the sum of this for a yearly average value
    d_x_year_total_avg = sum(dl_x_month_avgs)

    # we want to cumulative proportion for each month
    # first calculate the proportion for the months
    dl_x_avg_cumulative_proportions = [0] + [dl_x_month_avgs[i]/d_x_year_total_avg for i in range(1,len(dl_x_month_avgs))]

    # get the cumulative sum
    dl_x_avg_cumulative_proportions = np.cumsum(dl_x_avg_cumulative_proportions)

    # now we want the same but for each individual year, not just the averages
    # first calculate the proportion of the month/year total then do a cumulative sum
    df_x_cumulative_proportions = df_x_data.div(df_x_data.sum(axis=1), axis=0).cumsum(axis=1)

    # now we want the same cumulative proportion of the monthly averages as before but for the y data
    # first get the averages for the months
    if(s_strange_sheet == 'COL003'):
        # if doing COL003 (11315000) only average the y months from 1944 to present
        dl_y_month_avgs = [0] + df_y_data.loc[1944:i_y_end_year, :].mean(axis=0).tolist()
    elif(s_strange_sheet == 'DEE023'):
        # if doing DEE023, do the standard calculation for this step
        dl_y_month_avgs = [0] + df_y_data.loc[i_y_start_year:i_y_end_year, :].mean(axis=0).tolist()
    else:
        dl_y_month_avgs = [0] + df_y_data.loc[i_y_start_year:i_y_end_year, :].mean(axis=0).tolist()

    # get the sum of this for a yearly average value
    d_y_year_total_avg = sum(dl_y_month_avgs)

    # proportion for the months
    dl_y_avg_cumulative_proportions = [0] + [dl_y_month_avgs[i] / d_y_year_total_avg for i in range(1, len(dl_y_month_avgs))]

    # get the cumulative sum
    dl_y_avg_cumulative_proportions = np.cumsum(dl_y_avg_cumulative_proportions)

    # now for every value in df_x_cumulative_proportions, we want the smallest value in dl_x_avg_cumulative_proportions
    # that is greater than or equal to the value
    # np.searchsorted does this with side set to 'left' for a greater than or equal to
    il_indices = np.searchsorted(dl_x_avg_cumulative_proportions, df_x_cumulative_proportions, side='left')

    # now if we ever had any that landed at the end they would be set to len(dl_x_avg_cumulative_proportions) but we want them to be len(dl_x_avg_cumulative_proportions) - 1 so we don't go out of bounds
    il_indices = np.clip(il_indices, 0, len(dl_x_avg_cumulative_proportions) - 1)


    df_factors = pd.DataFrame(
        np.where((dl_x_avg_cumulative_proportions[il_indices] - dl_x_avg_cumulative_proportions[il_indices - 1]) == 0,
                 (df_x_cumulative_proportions - dl_x_avg_cumulative_proportions[il_indices - 1]) / (
                             dl_x_avg_cumulative_proportions[il_indices] - dl_x_avg_cumulative_proportions[
                         il_indices - 1] + 0.000001),
                 (df_x_cumulative_proportions - dl_x_avg_cumulative_proportions[il_indices - 1]) / (
                             dl_x_avg_cumulative_proportions[il_indices] - dl_x_avg_cumulative_proportions[
                         il_indices - 1])),
        columns=df_x_cumulative_proportions.columns, index=df_x_cumulative_proportions.index)

    # now use these factors get df_y_cumulative_proportions by doing the reverse of that operation but with dl_y_avg_cumulative_proportions instead of dl_x_avg_cumulative_proportions
    # these are the scaled version of the df_x_cumulative_proportions numbers
    df_y_cumulative_proportions = dl_y_avg_cumulative_proportions[il_indices- 1] + df_factors * (dl_y_avg_cumulative_proportions[il_indices] - dl_y_avg_cumulative_proportions[il_indices- 1])

    # now we will fit a linear regression on all the data we have y data for even if it's larger than the y window
    # first get the year totals
    df_x_year_totals = pd.DataFrame(df_x_data.sum(axis=1))
    df_y_year_totals = pd.DataFrame(df_y_data.sum(axis=1))

    if s_strange_sheet == "DEE023":
        df_y_year_totals.drop(index=1967, inplace=True)
    # fit a model and get the slope and intercept
    o_lin_model = LinearRegression()
    o_lin_model.fit(df_x_year_totals.loc[df_y_year_totals.index,], df_y_year_totals)
    d_slope = o_lin_model.coef_[0][0]
    d_intercept = o_lin_model.intercept_[0]

    # get the scaled y yearly totals
    df_y_year_totals_scaled = df_x_year_totals * d_slope + d_intercept

    # multiply df_y_cumulative_proportions by the scaled yearly totals to get df_y_cumulative_totals which is the equivalent of df_x_data after the cumulative sum
    df_y_cumulative_totals = df_y_cumulative_proportions.mul(df_y_year_totals_scaled.values, axis=0)

    # do the reverse of a cumulative sum to get the scaled version of df_x_data
    df_y_data_synthetic = pd.DataFrame(np.diff(df_y_cumulative_totals, prepend=0), index=df_x_data.index, columns=df_x_data.columns)

    # put the range of original y to keep back in
    df_y_data_output = df_y_data_synthetic.copy()

    # if df_y_data, put all y data back in
    if b_use_all_y:
        df_y_data_output.loc[df_y_data.index, :] = df_y_data

    # otherwise just the y years range
    else:
        df_y_data_output.loc[i_y_start_year:i_y_end_year, :] = df_y_data.loc[i_y_start_year:i_y_end_year, :]

    # save stats if indicated
    # add a line to the output csv with location,slope,intercept
    if b_save_stats:
        df_stats = pd.DataFrame(
            {'reference location':[s_reference_name]*2,
            'target location':[s_target_name]*2,
            'stat':['slope','intercept'],
            'value':[d_slope,d_intercept]})
        df_stats.to_csv(s_out_stats,mode='a',index=False,header=False) 

    return df_y_data_output, df_y_data_synthetic


def s_curve_comparison_plots(df_final_y_dat, df_y_data_synthetic, df_x_data, df_y_data, s_current_location,s_reference_location,
                            b_save_stats=False,s_out_stats = 'Outputs/SCurveStats.csv'):
    """
    Generates two plots to understand the quality of the generated data.
    First plot compares the historical y data and the reference x data.
    Second plot compares the historical y data and the synthetic y data.

    Parameters
    ----------
    df_final_y_dat: dataframe
        Final y data that is synthetic where data was missing and historical where we had the data
    df_y_data_synthetic: dataframe
        Fully synthetic y data
    df_x_data: dataframe
        Original x data
    df_y_data: dataframe
        Original y data
    s_current_location: str
        Current location of the data
    s_reference_location: str
        Reference location name
    b_save_stats: boolean
        Option to save s-curve stats
    s_out_stats: string
        Output file to save s-curve stats if b_save_stats is true
    Returns
    -------
    None
    """

    # save dataset names


    # first remove nans so they wont get plotted as zeros
    df_x_data.dropna(inplace=True)
    df_y_data.dropna(inplace=True)

    # get the years months when the data overlaps
    o_overlaps = df_y_data.index.intersection(df_x_data.index)

    # first plot looks at yearly totals for where we have y data
    df_x_totals = df_x_data.sum(axis=1)[o_overlaps]
    df_y_totals = df_y_data.sum(axis=1)[o_overlaps]

    # scatter plot of this data with labels of the years
    plt.figure(figsize=(10, 5))
    plt.scatter(df_x_totals.values, df_y_totals.values, marker='.', color='royalblue')
    for x,y,label in zip(df_x_totals.values, df_y_totals.values, df_y_totals.index.values):
        plt.text(x,y,label, ha='center', va='bottom', size='x-small')

    # fit a line of best fit
    slope, intercept = np.polyfit(df_x_totals.values, df_y_totals.values, 1)
    dl_line_vals = intercept + slope * df_x_totals.values
    r2 = r2_score(df_y_totals.values, dl_line_vals)

    # plot line of best fit
    # show the formula for the line and the r squared value as the label

    plt.plot(df_x_totals.values, dl_line_vals, color='black', linewidth=0.5, label=f'y = {slope:.4f}x + {intercept:.4f}\nR^2 = {r2:.4f}')

    # formatting of plot
    plt.grid(alpha=0.5)
    plt.xlim((0,None))
    plt.ylim(0,None)
    plt.xlabel('Reference Data Flows (TAF)')
    plt.ylabel(f'{s_current_location} Flows (TAF)')
    # plt.title('Correlation of Annual Flows (TAF)')
    plt.legend()
    plt.savefig(f'./Figures/{s_current_location} Correlation of Annual Reference vs Current Flows', bbox_inches='tight', dpi=300)
    plt.close()

    # second plot looks at the final y data compared the fully synthetic y data
    # get the original y data and the synthetic to timeseries
    df_y_data_timeseries = monthly_to_timeseries(df_y_data)
    df_y_data_synthetic_timeseries = monthly_to_timeseries(df_y_data_synthetic)

    # trim the dataframes to only have the common dates
    df_y_data_timeseries = df_y_data_timeseries.loc[df_y_data_timeseries.index.isin(df_y_data_synthetic_timeseries.index)]
    df_y_data_synthetic_timeseries = df_y_data_synthetic_timeseries.loc[df_y_data_synthetic_timeseries.index.isin(df_y_data_timeseries.index)]

    plt.figure(figsize=(10, 5))
    plt.fill_between(df_y_data_timeseries.index, df_y_data_timeseries['TAF'], color='royalblue', label='Historical')
    plt.plot(df_y_data_synthetic_timeseries.index, df_y_data_synthetic_timeseries['TAF'], color='red', linewidth=0.5, label='Computed Flows')

    # formatting of plot
    plt.ylim((0,None))
    plt.legend()
    plt.grid(alpha=0.5)
    plt.ylabel(f'{s_current_location} Monthly Flow (TAF)')
    plt.savefig(f'./Figures/{s_current_location} Monthly Flows Observed vs Synthetic', bbox_inches='tight', dpi=300)
    plt.close()

    # save stats if indicated
    # add a line to the output csv with location,slope,intercept
    if b_save_stats:
        df_stats = pd.DataFrame(
            {'reference location':[s_reference_location]*3,
            'target location':[s_current_location]*3,
            'stat':['fit_slope','fit_intercept','r2'],
            'value':[slope,intercept,r2]})
        df_stats.to_csv(s_out_stats,mode='a',index=False,header=False) 

def read_data(s_path):
    """
    Reads in CSV data, formats it, and adds TAF
    Parameters
    ----------
    s_path: str
        Path to CSV file

    Returns
    -------
    df_data: dataframe
        Data from the CSV file
    """

    # read in the csv data with the first column as the index and looking for dates
    df_data = pd.read_csv(s_path, index_col=0, parse_dates=True)

    # -901 is the missing data representation, change to nans
    df_data.replace(-901, np.nan, inplace=True)

    # if TAF is not in there already we will try to add it
    if 'TAF' not in df_data.columns:

        # if TAF just lowercase, update the column name
        if 'taf' in df_data.columns:
            df_data.rename(columns={'taf': 'TAF'}, inplace=True)

        # if cfs is in the columns, do the conversion
        elif 'cfs' in df_data.columns:
            df_data['TAF'] = df_data['cfs'] * df_data.index.day * 24 * 60 * 60 / (220 * 22 * 9 * 1000)

        # same as cfs but if it is uppercase
        elif 'CFS' in df_data.columns:
            df_data['TAF'] = df_data['CFS'] * df_data.index.day * 24 * 60 * 60 / (220 * 22 * 9 * 1000)

    # return the dataframe
    return df_data.copy()


def unimpaired_flows(df_impaired, fl_storages=[], fl_additions=[], fl_subtractions=[]):
    """
    Unimpaired impaired flows. Little QA/QC for negative values then does impaired flow + storage difference + upstreams - downstreams

    Parameters
    ----------
    df_impaired: seires
        Impaired flow data
    fl_storages: list of series
        Storage data for the reservoirs upstream
    fl_additions: list of series
        Data that needs to be added in
    fl_subtractions: list of series
        Data that needs to be subtracted out

    Returns
    -------
    df_unimpaired: series
        Unimpaired flow data
    """

    if isinstance(df_impaired, pd.DataFrame):
        df_impaired = df_impaired['TAF']

    # for each data sets except for the impaired flow set anything below zero to zero
    for i_index, df_curr in enumerate(fl_storages):
        if isinstance(df_curr, pd.DataFrame):
            df_curr = df_curr['TAF']
        fl_storages[i_index] = df_curr.copy()
        fl_storages[i_index].loc[fl_storages[i_index]< 0] = 0

    for i_index, df_curr in enumerate(fl_additions):
        if isinstance(df_curr, pd.DataFrame):
            df_curr = df_curr['TAF']
        fl_additions[i_index] = df_curr.copy()
        fl_additions[i_index].loc[fl_additions[i_index] < 0] = 0

    for i_index, df_curr in enumerate(fl_subtractions):
        if isinstance(df_curr, pd.DataFrame):
            df_curr = df_curr['TAF']
        fl_subtractions[i_index] = df_curr.copy()
        fl_subtractions[i_index].loc[fl_subtractions[i_index]< 0] = 0

    # start with the impaired data
    df_unimpaired = df_impaired.copy()

    # for each reservoir we want to add in the difference in storage
    for df_storage in fl_storages:
        df_unimpaired = df_unimpaired + df_storage - df_storage.shift(1)

    # everything upstream gets added in
    for df_upstream in fl_additions:
        df_unimpaired = df_unimpaired + df_upstream

    # everything downstream gets subtracted out
    for df_downstream in fl_subtractions:
        df_unimpaired = df_unimpaired - df_downstream

    # return dataframe
    return df_unimpaired.copy()


def timeseries_to_monthly(df_timeseries):
    """
    Convert a dataframe from a regular timeseries to a dataframe with the water years as the rows and the months as the columns. Months in water year order.

    Parameters
    ----------
    df_timeseries: dataframe
        Timeseries data

    Returns
    -------
    df_monthly: dataframe
        Data in new format
    """
    # if it is a series, cover to a frame
    if isinstance(df_timeseries, pd.Series):
        df_timeseries_copy = df_timeseries.to_frame('TAF')
    else:
        # copy so we don't edit the original
        df_timeseries_copy = df_timeseries.copy()

    # add the month and water year
    df_timeseries_copy['Month'] = df_timeseries_copy.index.month
    df_timeseries_copy['Water Year'] = np.where(df_timeseries_copy.index.month < 10, df_timeseries_copy.index.year, df_timeseries_copy.index.year + 1)

    # create the output dataframe with the years as the rows and the months as the columns
    df_monthly = pd.DataFrame(index=df_timeseries_copy['Water Year'].unique(), columns=[10, 11, 12, 1, 2, 3, 4, 5, 6 ,7 ,8, 9], dtype='float')

    # loop through and insert the data
    for month in df_timeseries_copy['Month'].unique():
        df_monthly.loc[df_timeseries_copy[df_timeseries_copy['Month'] == month]['Water Year'], month] = df_timeseries_copy[df_timeseries_copy['Month'] == month]['TAF'].values

    # reset the column names, s curve disaggregation needs this
    df_monthly.columns = range(df_monthly.columns.size)

    # return the dataframe
    return df_monthly.copy()


def monthly_to_timeseries(df_monthly):
    """
    Convert a data from  a dataframe with the water years as the rows and the months as the columns to a regular timeseries. Months in water year order.

    Parameters
    ----------
    df_monthly: dataframe
        Data in year month format

    Returns
    -------
    df_timeseries: dataframe
        Timeseries data
    """
    df_monthly_copy = df_monthly.copy()

    # pull out the start and end dates
    o_start_date = datetime(year=df_monthly_copy.index[0]-1, month=10, day=31)
    o_end_date = datetime(year=df_monthly_copy.index[-1], month=9, day=30)

    # make a dataframe with the date range as the index
    df_timeseries = pd.DataFrame(index=pd.date_range(o_start_date, o_end_date, freq='ME'), columns=['TAF'], dtype='float')

    # add the month and water year in to match on
    df_timeseries['Month'] = df_timeseries.index.month
    df_timeseries['Water Year'] = np.where(df_timeseries.index.month < 10, df_timeseries.index.year, df_timeseries.index.year + 1)

    # reset the monthly data columns to the proper months
    df_monthly_copy.columns = [10, 11, 12, 1, 2, 3, 4, 5, 6 ,7 ,8, 9]

    # loop through the months and put the data into the timeseries dataframe
    for month in df_monthly_copy.columns:
        df_timeseries.loc[(df_timeseries['Month'] == month) & (df_timeseries['Water Year'].isin(df_monthly_copy.index)), 'TAF'] = df_monthly_copy[month].values

    # drop month and water year
    df_timeseries.drop(columns=['Month', 'Water Year'], inplace=True)

    # return the dataframe
    return df_timeseries.copy()


def remove_negatives(df_monthly):
    """
    Removes negative values while preserving the yearly totals. Distributes the 'negative water' over the rest of the months

    Parameters
    ----------
    df_monthly: dataframe
        Data in year month format

    Returns
    -------
    df_monthly_positive: dataframe
        Data with negatives removed
    """

    # first copy so we don't edit the original
    df_monthly_copy = df_monthly.copy()

    # get the columns before we add any
    li_columns = df_monthly_copy.columns.tolist()

    # get the yearly total and yearly total excluding negatives
    # replace 0s with nans, these come from summing only nans
    df_monthly_copy['Total TAF'] = df_monthly_copy[li_columns].sum(axis=1).replace(0, np.nan)
    df_monthly_copy['Pos Total TAF'] = df_monthly_copy[df_monthly_copy > 0][li_columns].sum(axis=1).replace(0, np.nan)

    # multiple original values by total/positive total
    df_monthly_positive = df_monthly_copy[li_columns].mul(df_monthly_copy['Total TAF'], axis=0).div(df_monthly_copy['Pos Total TAF'], axis=0)

    # remove the negative values
    df_monthly_positive[df_monthly_copy < 0] = 0

    return df_monthly_positive.copy()


def remove_negatives_timeseries(df_timeseries):
    """
    Removes negative values while preserving the water year totals. Distributes the 'negative water' over the rest of the months

    Parameters
    ----------
    df_timeseries: dataframe
        Original data, in timeseries format

    Returns
    -------
    df_timeseries_positive: dataframe
        Data with negatives removed
    """

    # start with a copy of the data
    df_timeseries_positive = df_timeseries.copy()

    # get the columns before we add any
    ls_cols = df_timeseries.columns.tolist()

    # get the water year
    df_timeseries_positive['Water Year'] = np.where(df_timeseries_positive.index.month < 10, df_timeseries_positive.index.year, df_timeseries_positive.index.year + 1)

    # get the yearly total and yearly total excluding negatives
    # replace 0s with nans, these come from summing only nans
    df_total = df_timeseries_positive.groupby(['Water Year'])[ls_cols].sum().replace(0, np.nan)
    df_pos_totals = df_timeseries_positive[df_timeseries_positive >0].groupby(['Water Year'])[ls_cols].sum().replace(0, np.nan)

    # set negatives to zero
    df_timeseries_positive[df_timeseries_positive < 0] = 0

    # add the totals back into the frame based on the water year
    df_timeseries_positive = df_timeseries_positive.merge(df_pos_totals, how='left', left_on='Water Year', right_index=True, suffixes=['', '_pos_tot'])
    df_timeseries_positive = df_timeseries_positive.merge(df_total, how='left', left_on='Water Year', right_index=True, suffixes=['', '_tot'])

    # for each column, multiply by total and divide byt the positive total to get the scaled values
    for col in ls_cols:
        df_timeseries_positive[col] = df_timeseries_positive[col] * df_timeseries_positive[col+'_tot'] / df_timeseries_positive[col+'_pos_tot']

    # remove all the extra columns we have created
    df_timeseries_positive = df_timeseries_positive[ls_cols]

    # return the positive frame
    return df_timeseries_positive


def area_scale(df_values, d_area_1, d_area_2):
    """
    Scales values by a ratio of the two areas.
    Parameters
    ----------
    df_values: dataframe
        Data to be scaled
    d_area_1: float
        Numerator area
    d_area_2: float
        Denominator area

    Returns
    -------
    df_values: dataframe
        Scaled data
    """

    if d_area_2 == 0:
        raise Exception('d_area_2 cannot be zero')

    return df_values * d_area_1 / d_area_2


def get_diversions(df_diversion_data_upstream, df_diversion_data_downstream, d_area_up, d_area_down):
    if isinstance(df_diversion_data_upstream, pd.DataFrame) and isinstance(df_diversion_data_downstream, pd.DataFrame):
        df_diversion_data_upstream = df_diversion_data_upstream['TAF']
        df_diversion_data_downstream = df_diversion_data_downstream['TAF']
    df_unimpaired_diversions = area_scale(df_diversion_data_upstream, d_area_down, d_area_up)
    df_final_diversions = df_unimpaired_diversions - df_diversion_data_downstream

    df_final_diversions.loc[df_final_diversions < 0] = 0
    return df_final_diversions.copy()


def create_final_flow_plots(df_final_flow, il_oberved_years, s_current_location):
    """
    Create the plots that are on the final flow sheet that show the observed vs derived data
    Parameters
    ----------
    df_final_flow: dataframe
        Final flow data
    il_oberved_years: list
        Water years that are observed data
    s_current_location: str
        Current location of the data

    Returns
    -------
    None
    """

    if isinstance(df_final_flow, pd.Series):
        df_final_flow_plotting = df_final_flow.to_frame('TAF').dropna()
    else:
        # copy the data frame so we don't edit it
        df_final_flow_plotting = df_final_flow.dropna().copy()

    # add in month and water year
    df_final_flow_plotting['Month'] = df_final_flow_plotting.index.month
    df_final_flow_plotting['Water Year'] = np.where(df_final_flow_plotting.index.month < 10, df_final_flow_plotting.index.year, df_final_flow_plotting.index.year + 1)

    # split into the observed and derived data
    df_observed = df_final_flow_plotting.loc[df_final_flow_plotting['Water Year'].isin(il_oberved_years)]
    df_derived =  df_final_flow_plotting.loc[~df_final_flow_plotting['Water Year'].isin(il_oberved_years)]

    # first plot is looking at yearly totals
    # sum by water year
    df_observed_year_avgs = df_observed.groupby('Water Year')['TAF'].sum()
    df_derived_year_avgs = df_derived.groupby('Water Year')['TAF'].sum()

    # get the long term average water year total
    d_long_term_avg = df_final_flow_plotting.groupby('Water Year')['TAF'].sum().mean()

    # now we will plot, start with setting the plot size
    plt.figure(figsize=(10, 5))

    # plot the derived and the observed
    plt.bar(df_derived_year_avgs.index, df_derived_year_avgs, color='lightblue', label ='Derived')
    plt.bar(df_observed_year_avgs.index, df_observed_year_avgs, color='royalblue', label='Observed')

    # plot the long term average
    plt.hlines(d_long_term_avg, df_final_flow_plotting['Water Year'].min(), df_final_flow_plotting['Water Year'].max(), color= 'darkblue', linestyle='--', label=f'Long Term Average ({s_current_location})')

    # format and save
    plt.ylabel('Total Flow (TAF)')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig(F'./Figures/{s_current_location} Annual Final Flows', bbox_inches='tight', dpi=300)
    plt.close()


    # next plot is looking at the monthly pattern
    # get the monthly averages for the derived, observed, and long term average
    df_observed_month_avgs = df_observed.groupby('Month')['TAF'].mean()
    df_derived_month_avgs = df_derived.groupby('Month')['TAF'].mean()
    df_long_term_avgs = df_final_flow_plotting.groupby('Month')['TAF'].mean()

    # if either of these are empty (no derived or no observed) set it to nans
    if df_derived_month_avgs.empty:
        df_derived_month_avgs = pd.Series(index=range(1, 13))
    if df_observed_month_avgs.empty:
        df_observed_month_avgs = pd.Series(index=range(1, 13))

    # set the bar width and month order to plot
    width=0.3
    il_month_order = [10, 11, 12, 1, 2, 3, 4, 5, 6 ,7 ,8, 9]
    sl_month_names = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

    # now we will plot, start with setting the plot size
    plt.figure(figsize=(10, 5))

    # plot the bars next to each other
    plt.bar(np.array(range(12)) + (width/2), df_derived_month_avgs[il_month_order], width=width, color='lightblue', label='Derived')
    plt.bar(np.array(range(12)) - (width/2), df_observed_month_avgs[il_month_order], width=width, color='royalblue', label='Observed')

    # plot the long term average as a line
    plt.plot(np.array(range(12)), df_long_term_avgs[il_month_order], color='darkblue', linestyle='--', label=f'Long Term Average ({s_current_location})')

    # use the month names as the x ticks
    plt.xticks(np.array(range(12)), sl_month_names)

    # format and save
    plt.ylabel('Monthly Average Flow (TAF)')
    plt.grid(alpha=0.5)
    plt.legend()
    plt.savefig(f'./Figures/{s_current_location} Monthly Average Final Flows', bbox_inches='tight', dpi=300)
    plt.close()


def flow_from_two_unimp(df_flow_default, df_secondary_flow, d_factor):
    """
    As an alternative to doing an s-curve disaggregation, some location use two flows to fill in the unimpaired flow for a location. One flow is the default but when that flow is missing the secondary flow is used and scaled.

    Parameters
    ----------
    df_flow_default: dataframe
        Default flow data to use
    df_secondary_flow: dataframe
        Secondary flow data to use
    d_factor: float
        Factor by which to scale the secondary flow by

    Returns
    -------
    df_final_flow: dataframe
        Combined flow data
    """
    # start with the default flow data
    df_final_flow = df_flow_default.copy()

    # anywhere where it is empty, fill with the secondary flow (scaled)
    df_final_flow.fillna(df_secondary_flow*d_factor, inplace=True)

    # return dataframe
    return df_final_flow.copy()


def pull_usgs_data(sl_stations, s_start_date, s_end_date):
    """
    Pulls USGS data for the given stations. Returns data straight from USGS and the data converted to monthly and TAF.
    Parameters
    ----------
    sl_stations: list
        USGS stations to pull data for
    s_start_date: str
        Start date of data
    s_end_date: str
        End date of data
    Returns
    -------
    df_gauge_data_original:dataframe
        Dataframe containing data from USGS data, unaltered
    df_gauge_data_monthly_taf: dataframe
        Dataframe containing data from USGS data converted to monthly TAF values
    """

    # append in USGS- to all  the stations
    sl_usgs_stations = ['USGS-' + station for station in sl_stations]

    # make the call to get the data
    df_usgs_data, metadata = waterdata.get_daily(
        monitoring_location_id=sl_usgs_stations,
        time=s_start_date + '/' + s_end_date,
        skip_geometry=True
    )

    # filter for the acre-feet data which will have param code 00054
    df_af_data = df_usgs_data[df_usgs_data['parameter_code'] == '00054']

    # format the data to have a colum for each location
    df_af_data = df_af_data.pivot(index='time', columns='monitoring_location_id', values='value')

    # format the index
    df_af_data.index = pd.to_datetime(df_af_data.index).tz_localize(None)
    df_af_data.sort_index(inplace=True)

    # filter for the cfs data which will have param code 00060
    df_cfs_data = df_usgs_data[df_usgs_data['parameter_code'] == '00060']

    # format the data to have a colum for each location
    df_cfs_data = df_cfs_data.pivot(index='time', columns='monitoring_location_id', values='value')

    # format the index
    df_cfs_data.index = pd.to_datetime(df_cfs_data.index).tz_localize(None)
    df_cfs_data.sort_index(inplace=True)

    # concat the original data
    df_gauge_data_original = pd.concat([df_af_data, df_cfs_data], axis=1)

    # remove name on index
    df_gauge_data_original.index.name = None

    # remove USGS- from column names
    df_gauge_data_original.columns = [station.split('-')[1] for station in df_gauge_data_original.columns]

    # resample to monthly and convert acre-feet to TAF
    df_af_data = df_af_data.resample('ME').last()
    df_af_data = df_af_data / 1000

    # resample to monthly and convert cfs to TAF
    df_cfs_data = df_cfs_data.resample('ME').mean()
    df_cfs_data = df_cfs_data.mul(df_cfs_data.index.day *  24 * 60 * 60 / (220 * 22 * 9 * 1000), axis=0)

    # combine TAF monthly data
    df_gauge_data_monthly_taf = pd.concat([df_af_data, df_cfs_data], axis=1)

    # remove name on index
    df_gauge_data_monthly_taf.index.name = None

    # remove USGS- from column names
    df_gauge_data_monthly_taf.columns = [station.split('-')[1] for station in df_gauge_data_monthly_taf.columns]

    print("Pulled data for USGS stations: ", list(df_gauge_data_monthly_taf.columns))
    print("Did not pull data for USGS stations: ", list(set(sl_stations) - set(df_gauge_data_original.columns)))

    # return the two dataframes
    return df_gauge_data_original, df_gauge_data_monthly_taf


def pull_cdec_data(sl_stations, s_start_date, s_end_date):
    s_start_date = datetime.strptime(s_start_date, '%Y-%m-%d').strftime('%Y-%m')
    s_end_date = datetime.strptime(s_end_date, '%Y-%m-%d').strftime('%Y-%m')

    # data frame to hold data straight from CDEC
    df_gauge_data_original = pd.DataFrame()

    # data frame to hold the monthly data in TAF
    df_gauge_data_monthly_taf = pd.DataFrame()

    for station in sl_stations:

        # construct the url to get the CDEC data
        s_url = f"https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations={station}&SensorNums=65&dur_code=M&Start={s_start_date}&End={s_end_date}"
        s_units = 'AF'

        # get the data
        # Make the request, retrying up to 5 times if connection fails
        i_num_tries = 0
        while i_num_tries <= 5:
            try:
                i_num_tries += 1
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                o_outflow_file = urllib.request.urlopen(s_url, timeout=60, context=ssl_context)
                s_outflow_file = o_outflow_file.read().decode('utf-8')
                break
            except urllib.error.URLError:
                time.sleep(1)
                s_outflow_file = ''
                continue

        # we if have something too short to be real, try again with a different url
        if s_outflow_file == '' or len(s_outflow_file) < 100:

            # construct the url to get the CDEC data
            s_url = f"https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations={station}&SensorNums=15&dur_code=M&Start={s_start_date}&End={s_end_date}"
            s_units = 'AF'

            # get the data
            # Make the request, retrying up to 5 times if connection fails
            i_num_tries = 0
            while i_num_tries <= 5:
                try:
                    i_num_tries += 1
                    ssl_context = ssl.create_default_context(cafile=certifi.where())
                    o_outflow_file = urllib.request.urlopen(s_url, timeout=60, context=ssl_context)
                    s_outflow_file = o_outflow_file.read().decode('utf-8')
                    break
                except urllib.error.URLError:
                    time.sleep(1)
                    s_outflow_file = ''
                    continue

            # we if have something too short to be real, try again with a different url
            if s_outflow_file == '' or len(s_outflow_file) < 100:

                # construct the url to get the CDEC data
                s_url = f"https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations={station}&SensorNums=110&dur_code=D&Start={s_start_date}-01&End={s_end_date}-30"
                s_units = 'CFS'

                # get the data
                # Make the request, retrying up to 5 times if connection fails
                i_num_tries = 0
                while i_num_tries <= 5:
                    try:
                        i_num_tries += 1
                        ssl_context = ssl.create_default_context(cafile=certifi.where())
                        o_outflow_file = urllib.request.urlopen(s_url, timeout=60, context=ssl_context)
                        s_outflow_file = o_outflow_file.read().decode('utf-8')
                        break
                    except urllib.error.URLError:
                        time.sleep(1)
                        s_outflow_file = ''
                        continue

        # if the connection never worked, skip this station
        if s_outflow_file == '' or len(s_outflow_file) < 100:
            print(f"Failed to pull CDEC data for: {station}")
            continue

        print(f"Pulled CDEC data for: {station}")

        # read this in like a CSV with only the date and value
        df_current = pd.read_csv(io.StringIO(s_outflow_file), index_col=0, parse_dates=True, sep=',', header=0, usecols=['DATE TIME', 'VALUE'])

        df_gauge_data_original = df_gauge_data_original.join(df_current['VALUE'].to_frame(station), how='outer')

        if s_units == 'AF':
            # this data is monthly so it just needs to be moved to the end of the month and divided by 1000
            # groupby and mean in case its more than monthly or not exactly on the first of the month but this should just move the data to the end of the month
            df_gauge_data_monthly_taf = df_gauge_data_monthly_taf.join((df_current.groupby(pd.Grouper(freq='ME')).mean()['VALUE'] / 1000).to_frame(station), how='outer')

        elif s_units == 'CFS':

            # this data is daily
            df_current = df_current.resample('ME').mean()
            df_current = df_current.mul(df_current.index.day * 24 * 60 * 60 / (220 * 22 * 9 * 1000), axis=0)
            df_gauge_data_monthly_taf = df_gauge_data_monthly_taf.join(
                df_current.rename(columns= {'VALUE': station}), how='outer')

    # remove the name from the index for both data frames
    df_gauge_data_original.index.name = None
    df_gauge_data_monthly_taf.index.name = None

    # return the functions
    return df_gauge_data_original, df_gauge_data_monthly_taf


def read_previous_data(s_path, df_new_data):
    """
    Read in the previous data and combine it with the new data
    Parameters
    ----------
    s_path:str
        Path to previous data file
    df_new_data: dataframe
        Dataframe containing new data from USGS data

    Returns
    -------
    df_all_data: dataframe
        Dataframe containing old and new data combined
    """
    # read the CSV
    df_previous_data = pd.read_csv(s_path, index_col=0, parse_dates=True)

    # set -901 to nan
    df_previous_data.replace(-901, np.nan, inplace=True)

    df_all_data = pd.concat([df_previous_data, df_new_data], axis=0)

    # drop any duplicated indices, keep the first not the second
    # this means any overlapping dates will be droped and the previous data will be kept, not the new data
    df_all_data = df_all_data.loc[~df_all_data.index.duplicated(keep='first'), :]

    # return the combined data
    return df_all_data


def extend_data(df_reference_data, df_current_data, df_extended_data, df_synthetic_data,
                i_y_start_year, i_y_end_year, b_use_all_y_data, s_name, i_x_start_year=1922,
                i_final_year=2021, s_strange_sheet='',b_save_stats=False):

    """
    Extends data using the s-curve disaggregation. Also creates the plots and saves the data into dataframes.

    Parameters
    ----------
    df_reference_data: series
        Reference pandas series
    df_current_data: series
        Current dataset series to be extended
    df_extended_data: dataframe
        Already extended data
    df_synthetic_data: dataframe
        Extended fully synthetic data
    i_y_start_year: int
        Start year for current data
    i_y_end_year: int
        End year for current data
    b_use_all_y_data: bool
        Flag for if we want to use all of the y data instead of just the selected years
    s_name: str
        Name of current station
    i_final_year: int
        Final year for the x data
    s_strange_sheet: string
        For a few sheets with strange modifications to the s-curve procedure, this is the sheet name with capital letters.
    b_save_stats: boolean
        Option to save stats of fitted s-curve
    
    Returns
    -------
    None
    """
    # do the s-curve disaggregation
    df_curr_final_data, df_curr_synthetic_data = s_curve_disaggregation(df_reference_data,
                                                                        df_current_data,
                                                                        i_x_start_year, i_final_year,
                                                                        i_y_start_year, i_y_end_year,
                                                                        b_use_all_y_data, s_strange_sheet,
                                                                        s_target_name = s_name,
                                                                        s_reference_name= df_reference_data.name,
                                                                        b_save_stats=b_save_stats)
    # generate the comparison plots
    s_curve_comparison_plots(df_curr_final_data, df_curr_synthetic_data,
                             timeseries_to_monthly(df_reference_data), timeseries_to_monthly(df_current_data),
                             s_name,df_reference_data.name,b_save_stats=b_save_stats)

    # put the data into the two final dataframes
    df_extended_data[s_name] = monthly_to_timeseries(df_curr_final_data)
    df_synthetic_data[s_name] = monthly_to_timeseries(df_curr_synthetic_data)

def extend_data_multi_model(df_reference_data_1, df_current_data_1, df_reference_data_2, df_current_data_2,
                df_extended_data, df_synthetic_data,
                i_y1_start_year, i_y1_end_year, i_y2_start_year, i_y2_end_year, b_use_all_y_data, s_name,
                s_model_name_1, s_model_name_2, i_x_start_year=1922,
                i_final_year=2021, s_strange_sheet='',b_save_stats=False):

    """
    Extends data using the s-curve disaggregation and compares two different models.
    Also creates the plots and saves the data into dataframes.

    Parameters
    ----------
    df_reference_data_1: series
        Reference pandas series, for running model 1
    df_current_data_1: series
        Current dataset series to be extended, for running model 1
    df_reference_data_2: series
        Reference pandas series, for running model 2
    df_current_data_2: series
        Current dataset series to be extended, for running model 2
    df_extended_data: dataframe
        Already extended data
    df_synthetic_data: dataframe
        Extended fully synthetic data
    i_y1_start_year: int
        Start year for current data, model 1
    i_y1_end_year: int
        End year for current data
    i_y2_start_year: int
        Start year for current data, model 1
    i_y2_end_year: int
        End year for current data
    b_use_all_y_data: bool
        Flag for if we want to use all of the y data instead of just the selected years
    s_name: str
        Name of current station
    i_final_year: int
        Final year for the x data
    s_strange_sheet: string
        For a few sheets with strange modifications to the s-curve procedure, this is the sheet name with capital letters.
    b_save_stats: boolean
        Option to save stats of fitted s-curve
    Returns
    -------
    None
    """
    # do the s-curve disaggregation for model 1
    df_curr_final_data_1, df_curr_synthetic_data_1 = s_curve_disaggregation(df_reference_data_1,
                                                                        df_current_data_1,
                                                                        i_x_start_year, i_final_year,
                                                                        i_y1_start_year, i_y1_end_year,
                                                                        b_use_all_y_data, s_strange_sheet,
                                                                        s_target_name = s_name + '_ref1',
                                                                        s_reference_name= df_reference_data_1.name,
                                                                        b_save_stats=b_save_stats)
    # do the s-curve disaggregation for model 2
    df_curr_final_data_2, df_curr_synthetic_data_2 = s_curve_disaggregation(df_reference_data_2,
                                                                            df_current_data_2,
                                                                            i_x_start_year, i_final_year,
                                                                            i_y2_start_year, i_y2_end_year,
                                                                            b_use_all_y_data, s_strange_sheet,
                                                                            s_target_name = s_name + '_ref2',
                                                                            s_reference_name = df_reference_data_2.name,
                                                                            b_save_stats=b_save_stats)

    # generate the comparison plots
    two_s_curves_comparison_plots(df_curr_final_data_1, timeseries_to_monthly(df_reference_data_1),
                                  df_curr_final_data_2, timeseries_to_monthly(df_reference_data_2), s_name,
                                  s_model_name_1, s_model_name_2,s_ref_name_1 = df_reference_data_1.name, 
                                  s_ref_name_2 = df_reference_data_2.name,b_save_stats=b_save_stats)

    # put the data into the two final dataframes
    df_extended_data[s_name+s_model_name_1] = monthly_to_timeseries(df_curr_final_data_1)
    df_synthetic_data[s_model_name_1] = monthly_to_timeseries(df_curr_synthetic_data_1)

    # put the data into the two final dataframes
    df_extended_data[s_name+s_model_name_2] = monthly_to_timeseries(df_curr_final_data_2)
    df_synthetic_data[s_model_name_2] = monthly_to_timeseries(df_curr_synthetic_data_2)


def calculate_watershed_factors(s_path):

    # read in the watershed factors csv
    df_watershed_factors = pd.read_csv(s_path)

    df_watershed_factors.columns = ['Location', 'Area', 'Precipitation']

    # calculate the area and precip proportions
    df_watershed_factors['Area Proportion'] = df_watershed_factors['Area'] / df_watershed_factors['Area'].sum()
    df_watershed_factors['Precip Proportion'] = df_watershed_factors['Precipitation'] / df_watershed_factors['Precipitation'].sum()
    df_watershed_factors['Factor'] = df_watershed_factors['Area Proportion'] * df_watershed_factors['Precip Proportion'] / (df_watershed_factors['Area Proportion'] * df_watershed_factors['Precip Proportion']).sum()

    return df_watershed_factors


def gap_fill(df_data, c_locations, i_final_year):
    """
    Gap fill the specified locations with monthly averages.

    Parameters
    ----------
    df_data: dataframe
        Dataframe with data to be gap filled
    c_locations: dict
        Dictionary of locations and water years to fill
    i_final_year: int
        Final year to consider for gap fill

    Returns
    -------
    None
    """

    # loop through the locations
    for location in c_locations:

        # pull out the location
        df_location = df_data[location].to_frame(location)

        # add month and water year in there
        df_location['Month'] = df_location.index.month
        df_location['Water Year'] = np.where(df_location.index.month < 10, df_location.index.year, df_location.index.year + 1)

        # calculate the monthly average
        df_monthly_averages = df_data.loc[:datetime(i_final_year, 9, 30), location].groupby(df_data.loc[:datetime(i_final_year, 9, 30), location].index.month).mean().to_frame('Mean')

        # merge temporarily to get the monthly value for each time step
        df_location = df_monthly_averages.merge(df_location, how='right', left_index=True, right_on='Month')

        # fill but only for the water years specified
        df_data.loc[df_location['Water Year'].isin(c_locations[location]), location] = df_location[location].fillna(df_location['Mean'])


def create_rim_inflow_comparison_plots(df_new, df_old):
    """
    Creates plots to compare two sets of rim inflows.
    Parameters
    ----------
    df_new: dataframe
        Dataframe with new rim inflows
    df_old: dataframe
        Dataframe with old rim inflows

    Returns
    -------
    None
    """

    # make the folder to hold the figures
    os.makedirs('./Figures/Comparison', exist_ok=True)

    # loop through each location
    for location in df_new.columns:

        # First plot is just the values
        # set figure size
        plt.figure(figsize=(10, 5))

        # Plot the data
        plt.fill_between(df_old.index, df_old[location], label='Previous Extension', color='royalblue')
        plt.fill_between(df_new.index, df_new[location], label='New Inflows', color='red', alpha=0.5)

        # format the plot
        plt.grid(alpha= 0.5)
        plt.legend(loc='upper left')
        plt.xlabel('Date')
        plt.ylabel('Rim Inflow (TAF)')
        plt.axis('tight')

        # save the figure
        plt.savefig(f'Figures/Comparison/{location}_comparison.png', bbox_inches='tight', dpi=300)
        plt.close()

        # next plot is looking at yearly totals
        # sum by water year
        df_old_year_sum = df_old.groupby(np.where(df_old.index.month < 10, df_old.index.year, df_old.index.year + 1)).sum()[location]
        df_new_year_sum = df_new.groupby(np.where(df_new.index.month < 10, df_new.index.year, df_new.index.year + 1)).sum()[location]

        # get the long term average water year total
        d_long_term_avg_old = df_old_year_sum.mean()
        d_long_term_avg_new = df_new_year_sum.mean()

        # now we will plot, start with setting the plot size
        plt.figure(figsize=(10, 5))

        # plot the derived and the observed
        plt.bar(df_old_year_sum.index, df_old_year_sum, color='royalblue', label='Previous Extension')
        plt.bar(df_new_year_sum.index, df_new_year_sum, color='red', alpha=0.5, label='New Inflows')

        # plot the long term average
        plt.hlines(d_long_term_avg_old, df_old_year_sum.index.min(), df_old_year_sum.index.max(), color='royalblue', linestyle='--',
                   label=f'Previous Extension Long Term Average')
        plt.hlines(d_long_term_avg_new, df_new_year_sum.index.min(), df_new_year_sum.index.max(), color='red', linestyle='--',
                   label=f'New Inflows Long Term Average')

        # format and save
        plt.ylabel('Water Year Total (TAF)')
        plt.grid(alpha=0.3)
        plt.legend(loc='upper left')
        plt.savefig(F'./Figures/Comparison/{location} Annual Flows', bbox_inches='tight', dpi=300)
        plt.close()

        # next plot is looking at the monthly pattern
        # get the monthly averages for the derived, observed, and long term average
        df_old_month_avgs = df_old.groupby(df_old.index.month)[location].mean()
        df_new_month_avgs = df_new.groupby(df_new.index.month)[location].mean()

        # set the bar width and month order to plot
        width = 0.3
        il_month_order = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        sl_month_names = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

        # now we will plot, start with setting the plot size
        plt.figure(figsize=(10, 5))

        # plot the bars next to each other
        plt.bar(np.array(range(12)) + (width / 2), df_old_month_avgs[il_month_order], width=width, color='royalblue', label='Previous Extension')
        plt.bar(np.array(range(12)) - (width / 2), df_new_month_avgs[il_month_order], width=width, color='red', label='New Inflows')

        # use the month names as the x ticks
        plt.xticks(np.array(range(12)), sl_month_names)

        # format and save
        plt.ylabel('Monthly Average Flow (TAF)')
        plt.grid(alpha=0.5)
        plt.legend(loc='upper left')
        plt.savefig(f'./Figures/Comparison/{location} Monthly Average', bbox_inches='tight', dpi=300)
        plt.close()


        plt.scatter(df_old[location].values, df_new[location].values, color='royalblue')
        plt.xlabel('Previous Extension (TAF)')
        plt.ylabel('New Inflows (TAF)')
        plt.grid(alpha=0.5)
        plt.axis('equal')
        plt.savefig(f'./Figures/Comparison/{location}', bbox_inches='tight', dpi=300)
        plt.close()

def sum_if_all_not_nan(df_target_data, s_sum_name, df_source_data, sl_source_names):
    """
    This function creates a new dataset by summing two or more sources of data, but only when all sources are not NaN
    Parameters
    ----------
    df_target_data: dataframe
        The dataframe where the result ends up.
    s_sum_name: string
        Column name in df_target_data where we will put the sum
    df_source_data: dataframe
        The dataframe that contains the items being summed.
    sl_source_names: list of strings
        List of column names for the source data sets

    Returns
    -------
    None
    """
    df_target_data[s_sum_name] = np.where(
        df_source_data[sl_source_names].notna().all(axis=1),
        df_source_data[sl_source_names].sum(axis=1),
        np.nan
    )

def compare_two_df(df_data_1, df_data_2, s_data_1_name, s_data_2_name):
    """
    This function prints some statements to the console about how similar two dataframe series are, element by
    element
    ----------
    df_data_1: dataframe
        The dataframe of one data set to be compared.
    df_data_2: dataframe
        The dataframe of the other data set to be compared.
    s_data_1_name: string
        The name of data_1 to be printed.
    s_data_2_name: string
        The name of data_2 to be printed.
    Returns
    -------
    None
    """

    # align and calculate differences
    aligned_1, aligned_2 = df_data_1.align(df_data_2, join='inner')
    d_diffs = (aligned_2 - aligned_1).abs().max()
    d_data_1_mean = df_data_1.mean()
    d_data_2_mean = df_data_1.mean()
    print("The mean for ", s_data_1_name, " is ", d_data_1_mean)
    print("The mean for ", s_data_2_name, " is ", d_data_2_mean)
    print("Their maximum difference is ", d_diffs)


def read_replication_data(ls_sheet_info, df_before, df_after):
    """
    This function prints some statements to the console about how similar two dataframe series are, element by
    element
    ----------
    ls_sheet_info: list of lists of strings
        each element in the main list is a list. within the inner list are three strings: a variable name to be used as
        the column name, the path to the "before" file, and the path to the "after" file.
    df_before: dataframe
        The dataframe where the "before" data ends up.
    df_after: dataframe
        The dataframe where the "after" data ends up.
    Returns
    -------
    None
    """
    # Custom month ordering starting with October
    c_month_map = {
        'Oct': 0, 'Nov': 1, 'Dec': 2,
        'Jan': 3, 'Feb': 4, 'Mar': 5,
        'Apr': 6, 'May': 7, 'Jun': 8,
        'Jul': 9, 'Aug': 10, 'Sep': 11
    }
    for sheet in ls_sheet_info:
        # create a column in df_before with the name of the excel sheet we're taking data from
        df_before[sheet[0]] = np.nan

        # read in the sheet
        df_temp = pd.read_csv(sheet[1], index_col=0)

        # convert index from 3 letter names to integers, Oct -> 0 ... Sep -> 11
        df_temp.columns = (df_temp.columns.map(c_month_map))

        # convert to timeseries and write into df_before
        df_before[sheet[0]] = monthly_to_timeseries(df_temp)

        # create a column in df_after with the name of the excel sheet we're taking data from
        df_after[sheet[0]] = np.nan

        # read in the sheet
        df_temp = pd.read_csv(sheet[2], index_col=0)

        # convert index from 3 letter names to integers, Oct -> 0 ... Sep -> 11
        df_temp.columns = (df_temp.columns.map(c_month_map))

        # convert to timeseries and write into df_after
        df_after[sheet[0]] = monthly_to_timeseries(df_temp)

def two_s_curves_comparison_plots(df_final_y_dat_1, df_x_data_1,
                                  df_final_y_dat_2, df_x_data_2, s_current_location, s_model_name_1, s_model_name_2,
                                  s_ref_name_1='',s_ref_name_2='',
                                  s_out_stats = 'Outputs/SCurveStats.csv',b_save_stats=False):
    """
    Generates a plot to compare model 1 and model 2 for a sheet.

    Parameters
    ----------
    df_final_y_dat_1: dataframe
        Final y data for model 1 that is synthetic where data was missing and historical where we had the data
    df_x_data_1: dataframe
        Original x data for model 1
    df_final_y_dat_2: dataframe
        Final y data for model 2 that is synthetic where data was missing and historical where we had the data
    df_x_data_2: dataframe
        Original x data for model 2
    s_current_location: str
        Current location of the data
    s_model_name_1: str
        The name for model 1
    s_model_name_2: str
        The name for model 2
    s_ref_name_1: str
        Reference gage name for model 1
    s_ref_name_2: str
        Reference gage name for model 2
    b_save_stats: boolean
        Option to save s-curve stats
    s_out_stats: string
        Output file to save s-curve stats if b_save_stats is true
    Returns
    -------
    None
    """
    # first remove nans so they won't get plotted as zeros
    df_x_data_1.dropna(inplace=True)

    # get the years months when the data overlaps
    o_overlaps_1 = df_final_y_dat_1.index.intersection(df_x_data_1.index)
    o_overlaps_2 = df_final_y_dat_2.index.intersection(df_x_data_1.index)

    # the plot looks at yearly totals for where we have y data
    # create yearly totals for both models, x and y
    df_x_totals_1 = df_x_data_1.sum(axis=1)[o_overlaps_1]
    df_y_totals_1 = df_final_y_dat_1.sum(axis=1)[o_overlaps_1]
    df_x_totals_2 = df_x_data_2.sum(axis=1)[o_overlaps_2]
    df_y_totals_2 = df_final_y_dat_2.sum(axis=1)[o_overlaps_2]


    # scatter plot of this data with labels of the years
    plt.figure(figsize=(10, 5))
    plt.scatter(df_x_totals_1.values, df_y_totals_1.values, marker='.', color='royalblue')
    plt.scatter(df_x_totals_2.values, df_y_totals_2.values, marker='.', color='red')

    # uncomment out these lines to add in year values next to data points
    # for x,y,label in zip(df_x_totals_1.values, df_y_totals_1.values, df_y_totals_1.index.values):
    #     plt.text(x,y,label, ha='center', va='bottom', size='x-small')

    # fit lines of best fit
    slope_1, intercept_1 = np.polyfit(df_x_totals_1.values, df_y_totals_1.values, 1)
    dl_line_vals_1 = intercept_1 + slope_1 * df_x_totals_1.values
    r2_1 = r2_score(df_y_totals_1.values, dl_line_vals_1)
    slope_2, intercept_2 = np.polyfit(df_x_totals_2.values, df_y_totals_2.values, 1)
    dl_line_vals_2 = intercept_2 + slope_2 * df_x_totals_2.values
    r2_2 = r2_score(df_y_totals_2.values, dl_line_vals_2)


    # plot the lines of best fit
    # show the formulas for the lines and the r squared values as the label

    plt.plot(df_x_totals_1.values, dl_line_vals_1, color='royalblue', linewidth=0.5, label=f'{s_model_name_1}\ny = {slope_1:.4f}x + {intercept_1:.4f}\nR^2 = {r2_1:.4f}')
    plt.plot(df_x_totals_2.values, dl_line_vals_2, color='red', linewidth=0.5, label=f'{s_model_name_2}\ny = {slope_2:.4f}x + {intercept_2:.4f}\nR^2 = {r2_2:.4f}')


    # formatting of plot
    plt.grid(alpha=0.5)
    plt.xlim((0,None))
    plt.ylim(0,None)
    plt.xlabel('Reference Data Flows (TAF)')
    plt.ylabel(f'{s_current_location} Flows (TAF)')
    # plt.title('Correlation of Annual Flows (TAF)')
    plt.legend()
    plt.savefig(f'./Figures/Model_Comparison/{s_current_location} Comparison of Two Models, {s_model_name_1} and {s_model_name_2}'
                , bbox_inches='tight', dpi=300)
    plt.close()

    # save stats if indicated
    # add a line to the output csv with location,slope,intercept
    if b_save_stats:
        df_stats = pd.DataFrame(
            {'reference location':[s_ref_name_1]*3+[s_ref_name_2]*3,
            'target location':[s_current_location + s_model_name_1]*3 + [s_current_location + s_model_name_2]*3,
            'stat':['fit_slope','fit_intercept','r2']*2,
            'value':[slope_1,intercept_1,r2_1,slope_2,intercept_2,r2_2]})
        df_stats.to_csv(s_out_stats,mode='a',index=False,header=False) 
