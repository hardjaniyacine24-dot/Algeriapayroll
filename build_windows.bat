@echo off
setlocal
cd /d "%~dp0"
title Algeria Payroll - Windows Builder

echo ==========================================
echo   Algeria Payroll - Build Windows Setup
echo ==========================================

where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python launcher not found.
  echo Install Python 3.11 x64 from https://www.python.org/downloads/windows/
  echo During installation, enable the Python Launcher option.
  pause
  exit /b 1
)

py -3 --version
if errorlevel 1 (
  echo ERROR: Python 3 could not be started.
  pause
  exit /b 1
)

py -3 -m pip install --upgrade pip
if errorlevel 1 goto :error
py -3 -m pip install pyinstaller
if errorlevel 1 goto :error
py -3 -m PyInstaller --noconfirm --clean --windowed --onefile --name AlgeriaPayroll --add-data "logo.png;." app.py
if errorlevel 1 goto :error

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if defined ISCC (
  "%ISCC%" installer.iss
  if errorlevel 1 goto :error
  echo.
  echo SUCCESS: installer_output\AlgeriaPayroll_Setup.exe
) else (
  echo.
  echo The application EXE was created in dist\AlgeriaPayroll.exe
  echo To create Setup.exe, install Inno Setup 6 from https://jrsoftware.org/isdl.php
  echo then run this file again.
)
pause
exit /b 0

:error
echo.
echo BUILD FAILED. Read the error above, then try again.
pause
exit /b 1
