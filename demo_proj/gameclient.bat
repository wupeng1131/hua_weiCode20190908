pushd %CD%
cd /d client
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "filename=log_%dt:~0,14%.txt"
start.bat > logs/%filename% 2>&1 %1 %2 %3
popd

