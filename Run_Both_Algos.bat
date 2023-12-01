@echo off

set path_py="C:\Users\LJ1105713\AppData\Local\Programs\Python\Python311\python.exe"
set file_1_2_py=".\1_Waiting_lists.py"
set file_2_2_py=".\4_Planification_week_ahead.py"

call %path_py% %file_1_2_py%
call %path_py% %file_2_2_py%

pause