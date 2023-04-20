setlocal enabledelayedexpansion

cd C:\FTP_root\DATA\acq2106_178\

for %%i in (*.dat) do (
    start /b python C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_178\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_178 --filename=%%i acq2106_178
)

cd C:\FTP_root\DATA\acq2106_377\

for %%i in (*.dat) do (
    start /b python C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_377\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_377 --filename=%%i acq2106_377
)




echo All child processes started

:WAIT_LOOP
:: check for any instances of the Python process that are still running
set "running=0"
for /f %%a in ('tasklist^|findstr /bi "python.exe"') do (
    set "running=1"
)

:: if any instances of the Python process are still running, wait for a short period before checking again
if %running% == 1 (
    timeout /t 1 /nobreak > nul
    goto WAIT_LOOP
)

echo All child processes finished



start /b "" python C:\FTP_root\Codes\slownmon_recombination.py


python C:\FTP_root\Codes\post_demux.py
