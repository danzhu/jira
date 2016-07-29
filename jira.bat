@echo off

:start
python U:\jira\jira.py
IF ERRORLEVEL 2 goto start
IF ERRORLEVEL 1 goto pause
EXIT

:pause
pause
goto start
