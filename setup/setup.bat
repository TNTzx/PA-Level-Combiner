@echo off
title PA Level Combiner: Setup


set codepath=%~dp0

call :getpath "%codepath%..\.py_embedded\python.exe"

echo Interpreter path: %interpreterpath%
echo Setup path: "%codepath%source.py"
echo.
echo Opening setup...

"%interpreterpath%" "%codepath%source.py"

echo Exiting setup...

exit


:getpath
    set interpreterpath=%~f1
    exit /b
