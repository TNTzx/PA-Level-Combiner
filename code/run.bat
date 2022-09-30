@echo off
color 0a
title PA Level Combiner


set codepath=%~dp0

call :getpath "%codepath%..\.py_embedded\pythonw.exe"
echo %interpreterpath%

"%interpreterpath%" "%codepath%main.py"


:getpath
    set interpreterpath=%~f1
    exit /b