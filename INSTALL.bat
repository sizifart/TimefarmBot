@Echo Off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
set "DEL=%%a"
)
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
call :colorEcho e0 "Please edit the data file (add query_id)."
echo.
pause
exit
:colorEcho
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1i