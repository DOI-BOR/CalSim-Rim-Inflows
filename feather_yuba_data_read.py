from extension_functions import *


if __name__ == "__main__":

    # this file reads in the upper american USGS and CDEC data amd combines it with the previous data

    # this holds the USGS data (sometimes gap filled) from the previous extension
    s_previous_data = r"./Inputs/feather_yuba_2022_extension_data.csv"

    s_station_list = r'./Inputs/feather_yuba_data_stations.csv'

    df_station_list = pd.read_csv(s_station_list, header=0, dtype=str)
    df_station_list = df_station_list.loc[df_station_list.Availability != "Not Needed (Historical)"]
    
    # USGS stations to pull data for: take unique list
    sl_usgs_stations = list(set(df_station_list[df_station_list['Source'] == 'USGS']['Station ID']))
    sl_cdec_stations = list(set(df_station_list[df_station_list['Source'] == 'CDEC']['Station ID']))
    sl_other_stations = list(set(df_station_list[df_station_list['Source'] == 'Other']['Station ID']))

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

    # save to csvs
    df_gauge_data_original.to_csv('./Intermediate/feather_yuba_gauge_data_original.csv')
    df_gauge_data_monthly_taf.to_csv('./Intermediate/feather_yuba_gauge_data_monthly_taf.csv')

    # combine the new data with the previous data
    df_full_data = read_previous_data(s_previous_data, df_gauge_data_monthly_taf)

    # The variations of the gage data from excel, should still use the same gage data for extension
    d_custom_gages = {
        "11414090_I_ENGLB": "11414090",
        "11414205_I_RLLNS": "11414205",
        "11414400_I_BOWMN": "11414400",
        "11414440_I_BOWMN": "11414440",
        "11414465_I_BOWMN": "11414465",
        "DS_CANAL_SPILLS_I_DER001": "DCN",
    }
    for s_custom, s_gage in d_custom_gages.items():
        df_full_data.loc[s_start_date:s_end_date, s_custom] = df_full_data.loc[s_start_date:s_end_date, s_gage]
    # Assume after 2003 abandoned (set values to 0)
    df_full_data.loc[s_start_date:s_end_date, "CHINA_DITCH"] = 0
    # 01/90 onwards Assume zero as diversion abandoned
    df_full_data.loc[s_start_date:s_end_date, "BVID_DIVERSION"] = 0
    # canal discontinued after 1967
    df_full_data.loc[s_start_date:s_end_date, "EXCELSIOR_DITCH"] = 0
    # Included in Cascade Canal After 1974
    df_full_data.loc[s_start_date:s_end_date, "SNOW_MOUNTAIN"] = 0
    
    # save to a csv
    df_full_data.to_csv('./Intermediate/feather_yuba_full_gauge_data.csv')
