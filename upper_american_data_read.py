from extension_functions import *


if __name__ == "__main__":

    # this file reads in the upper american USGS and CDEC data amd combines it with the previous data

    # this holds the USGS data (sometimes gap filled) from the previous extension
    s_previous_data = r".\Inputs\upper_american_2022_extension_data.csv"

    s_station_list = r'.\Inputs\upper_american_data_stations.csv'

    df_station_list = pd.read_csv(s_station_list, header=0)

    # USGS stations to pull data for
    sl_usgs_stations = df_station_list[df_station_list['Source'] == 'USGS']['Station ID'].to_list()
    sl_cdec_stations = df_station_list[df_station_list['Source'] == 'CDEC']['Station ID'].to_list()
    sl_other_stations = df_station_list[df_station_list['Source'] == 'Other']['Station ID'].to_list()

    # time range to pull USGS data for
    s_start_date = '2021-10-01'
    s_end_date = '2024-09-30'

    # first if the needed output folders don't exist, create them
    os.makedirs('./Intermediate', exist_ok=True)

    # pull USGS data
    df_usgs_data_original, df_usgs_data_monthly_taf = pull_usgs_data(sl_usgs_stations, s_start_date, s_end_date)

    # pull the cdec data
    df_cdec_data_original, df_cdec_data_monthly_taf = pull_cdec_data(sl_cdec_stations, s_start_date, s_end_date)

    # combine all the gauge data
    df_gauge_data_original = pd.merge(df_usgs_data_original, df_cdec_data_original, how='outer', left_index=True,
                                      right_index=True)
    df_gauge_data_monthly_taf = pd.merge(df_usgs_data_monthly_taf, df_cdec_data_monthly_taf, how='outer',
                                         left_index=True, right_index=True)

    df_gauge_data_monthly_taf.rename(columns={'BEV': 'YB90'}, inplace=True)

    # save to csvs
    df_gauge_data_original.to_csv('./Intermediate/upper_american_gauge_data_original.csv')
    df_gauge_data_monthly_taf.to_csv('./Intermediate/upper_american_gauge_data_monthly_taf.csv')

    # combine the new data with the previous data
    df_full_data = read_previous_data(s_previous_data, df_gauge_data_monthly_taf)
    # save to a csv
    df_full_data.to_csv('./Intermediate/upper_american_full_gauge_data.csv')