@echo off

del /F "client.exe"
rmdir /Q /S "dist"
rmdir /Q /S "build"

pyinstaller --onefile "client.py"

if errorlevel 1 (
   echo [!] Error while building: client.exe
) else (
   echo [*] Successfully build: client.exe
)

move "dist\client.exe" .
del /F "client.spec"
rmdir /Q /S "dist"
rmdir /Q /S "build"
pause