@echo off
color 0a
title PA Level Combiner


set codepath=%~dp0

call :getpath "%codepath%..\.py_embedded\python.exe"

echo Interpreter path: %interpreterpath%
echo Launch path: "%codepath%launch.py"
echo Main path: "%codepath%main.py"
echo.
echo Opening program...

"%interpreterpath%" "%codepath%launch.py"

echo Exiting program...

exit


:getpath
    set interpreterpath=%~f1
    exit /b