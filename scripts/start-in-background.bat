@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd %ROOT_DIR%


REM start as separate process
SET "DEFAULT_TO_PORT9000=--port 9000"
start instrument-server %DEFAULT_TO_PORT9000% %* command_plugin_example.yaml
