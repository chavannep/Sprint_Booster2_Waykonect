@echo off
setlocal

set STARTTIME=%TIME%

echo ###########################################
echo #                                         #
echo    Computation : launched  at %STARTTIME%
echo #                                         #
echo ###########################################

set path_py="C:\Users\LJ1105713\AppData\Local\Programs\Python\Python311\python.exe"
set file_1_2_py=".\1_Waiting_lists.py"
set file_2_2_py=".\4_Planification_week_ahead.py"

echo ###########################################
echo #                                         #
echo         Step 1/2 : Waiting lists  
echo #                                         #
echo ###########################################
	
call %path_py% %file_1_2_py%

echo ###########################################
echo #                                         #
echo         Step 2/2 : Planification  
echo #                                         #
echo ###########################################

call %path_py% %file_2_2_py%

set ENDTIME0=%TIME%

rem convert STARTTIME and ENDTIME to centiseconds
set /A STARTTIME=(1%STARTTIME:~0,2%-1000)*3600000 + (1%STARTTIME:~3,2%-1000)*60000 + (1%STARTTIME:~6,2%-1000)*1000 + (1%STARTTIME:~9,2%-1000)
set /A ENDTIME=(1%ENDTIME0:~0,2%-1000)*3600000 + (1%ENDTIME0:~3,2%-1000)*60000 + (1%ENDTIME0:~6,2%-1000)*1000 + (1%ENDTIME0:~9,2%-1000)

rem calculating the duration is easy
set /A DURATION=%ENDTIME%-%STARTTIME%

rem now break the centiseconds down to hours, minutes, seconds and the remaining centiseconds
set /A DURATIONH=%DURATION% / 3600000
set /A DURATIONM=(%DURATION% - %DURATIONH%*3600000) / 60000
set /A DURATIONS=(%DURATION% - %DURATIONH%*3600000 - %DURATIONM%*60000) / 1000
set /A DURATIONHS=(%DURATION% - %DURATIONH%*3600000 - %DURATIONM%*60000 - %DURATIONS%*1000)

rem some formatting
if %DURATIONH% LSS 10 set DURATIONH=0%DURATIONH%
if %DURATIONM% LSS 10 set DURATIONM=0%DURATIONM%
if %DURATIONS% LSS 10 set DURATIONS=0%DURATIONS%
if %DURATIONHS% LSS 10 set DURATIONHS=0%DURATIONHS%

echo ###########################################
echo #                                         #
echo   Computation : finished at %ENDTIME0%% 
echo             after %DURATION% ms
echo #                                         #
echo ###########################################

pause
exit