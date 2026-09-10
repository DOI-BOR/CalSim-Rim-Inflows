# CalSim Rim Inflow Extension

***Please note that this repository has been released under a provisional release and is in no way a finished product. A significant amount of development is expected.***

Rim watersheds represent the foothill and mountain regions that drain into California’s Central Valley. The time series of these inflows are an input into CalSim 3. 
These inflows were developed from a variety of sources, including direct gauge measurements, correlations with streamflow records from adjacent watersheds, depletion analyses, reservoir operations reports, and reservoir simulation models.

These rim flow have previously been calculated in Excel worksheets, but now they are calculated using Python. 
The goal of this change is to increase clarity and reproducibility and decrease the amount of time and effort to do an extension of these time series. 
This work should also decrease the chance for errors since more is automated with Python. 

Along with transitioning into Python, there have been a few updates to the methods used to calculate the rim inflows. 
All the updates were done to improve consistency across inflows.


## Current Status
The Upper American Basin has been completed. First it was replicated (see american-replicated tag) and then a few improvements around multiple versions of the data were made.
All the Upper American related files are named with the 'upper_american_' prefix.

The *upper_american_2022_extension_data.csv* file contains the data used in the previous extension. Where possible, the gap filling was removed and moved to be done in the code. Places where the DWR COMP model was used, were not removed.

## Calculating Rim Inflows

### To create an environment

`conda env create -f environment.yml`

`conda activate extension`

### To run the full rim inflow dataset calculations

To run the full set of rim inflow scripts, run the run_rim_inflows.bat script. This batch file will run all rim inflows calculations for all locations within this respository as well as a summary script to caclutate summary metrics for all rim inflows.

### To recreate the rim inflows for a basin with the data in the repository:

Run `python upper_american_data_read.py` to read in the data and then `python upper_american_calculate_rim_inflows.py` to calculate the rim inflows.

The calculated flows will be in the *Outputs* folder in *upper_american_rim_inflows.csv*.

### To do an extension:
1. Update any data that cannot be automatically pulled. Put this into the *Inputs* folder. You may need to add reading this data in to the code.
2. In *upper_american_calculate_rim_inflows.py*, update `i_final_year` to the final water year to include.
3. Run `python upper_american_data_read.py` to read in the data and then `python upper_american_calculate_rim_inflows.py` to calculate the rim inflows.

The calculated flows will be in the *Outputs* folder in *rim_inflows.csv*.

### To run summary statistics
Run `python Summary_statistics.py` to calculate summary statistics for each rim inflow location. *Note rim inflows must be calculated prior to running the summary script

## Developing Rim Inflows

### To incorporate additional locations
Every location is different so the process to incorporate a new location is going to look different every time. For a new basin, create a new set of files named with the basin name. Generally, the following this must be added:
1. Any data from the previous extension should be added, in TAF, to *Inputs/upper_american_2022_extension_data.csv*
2. Any USGS or CDEC stations should be added to *upper_american_data_stations.csv*
3. If any new reservoirs are needed, an evaporation function should be created in *evaporation_functions.py* and called in *upper_american_calculate_rim_inflows.py*
4. If data needs to be unimpaired, a function should be created in *unimpairment_functions.py* and called in *upper_american_calculate_rim_inflows.py*
5. If data needs to be extended, a call to *extend_data* should be added in *upper_american_calculate_rim_inflows.py*
6. A final rim inflow function should be created in *rim_inflow_functions.py* and called in *upper_american_calculate_rim_inflows.py*

## Reference Documentation
For more information on the methods used to calculate the rim inflows see chapter 5 of the CalSim 3 Hydrology Report on the [CalSim website](https://water.ca.gov/Library/Modeling-and-Analysis/Central-Valley-models-and-tools/CalSim-3).
Specific documentation for the transition to using Python is in the process of being created.