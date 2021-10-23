@echo off
COLOR 0A
set root=%HOMEPATH%\Anaconda3
call %root%\Scripts\activate.bat %root%
@echo on
pip install --user -r requirements.txt
pause