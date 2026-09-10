@echo off 

:: Start Python Environment
echo Starting Python Environment
call conda activate extension

:: Remove previous output files series of steps to ensure the correct files are deleted
echo WARNING removing previous output files
pause

set "TARGET_FOLDER=Outputs"
set "FULL_PATH=%~dp0%TARGET_FOLDER%"

if "%TARGET_FOLDER%"=="" (
    echo ERROR: TARGET_FOLDER variable is empty! Aborting.
    pause
    exit /b
)
if not exist "%FULL_PATH%\" (
    echo ERROR: Target folder "%FULL_PATH%" does not exist! Aborting.
    pause
    exit /b
)

del /f /q "%FULL_PATH%\*.*"
echo Done! All files deleted safely.
pause


echo Starting Rim Inflow Python script sequence

:: Upper American
echo Running Upper American Module
python  upper_american_data_read.py
python upper_american_calculate_rim_inflows.py

:: Upper Mokelumne
echo Running Upper Mokelumne
python upper_mokelumne_data_read.py
python upper_mokelumne_calculate_rim_inflows.py

:: Generate Summary Tables and Figures
echo Summarizing Rim Inflow Output
python Summary_statistics.py
pause
