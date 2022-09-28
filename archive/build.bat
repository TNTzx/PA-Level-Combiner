@echo off
color 0a
title Build!


set /p venv="Enter Python 3.10.1 venv Scripts path (No ending slash) (No input to get path from default_venv_path.txt): "

if "%venv%" NEQ "" goto execute_stuff
set /p venv=<default_venv_path.txt

:execute_stuff
echo %venv%
"%venv%\pyinstaller.exe" ./main.spec --clean --workpath="..\exes\output" --distpath="..\exes\output"
pause
