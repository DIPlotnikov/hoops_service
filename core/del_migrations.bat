@echo off
echo Searching for migration files...

for /r "%cd%" %%f in (*.py) do (
    if /I "%%~nxf"=="__init__.py" (
        rem skip
    ) else (
        echo Checking %%f | findstr /i "\\migrations\\" >nul
        if not errorlevel 1 (
            del /q "%%f"
            echo Deleted: %%f
        )
    )
)

for /r "%cd%" %%f in (*.pyc) do (
    echo Checking %%f | findstr /i "\\migrations\\" >nul
    if not errorlevel 1 (
        del /q "%%f"
        echo Deleted: %%f
    )
)

echo Done. All migration files deleted except __init__.py
pause
