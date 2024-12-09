@echo off

REM receive arg as options

IF "%1" == "act" (
    call venv\Scripts\activate
)

IF "%1" == "arun" (
    call venv\Scripts\activate & python run.py
) 

IF "%1" == "start" (
    IF exist "venv\" ( 
        echo "Virtual environment already exists. Skipping..."

    ) ELSE (
        echo "Creating virtual environment and installing dependences..."
        python -m venv venv & call venv\Scripts\activate & pip install -r requirements.txt
    )

    echo "Checking for default directories..."
    IF exist "example\" (
        echo "Default directories already exists. Skipping..."

    ) ELSE (
        echo "Creating default directories..."

        mkdir example & mkdir example\default_savepath & mkdir example\default_search
        python pyxl_start.py

    )
    echo "Starting server..."
    start cmd /C "pyxl.bat arun"
)

IF "%1" == "dea" (
    deactivate
)

IF "%1" == "run" (
    python run.py 
)

IF "%1" == "deb" (
    python run.py -d
)

IF "%1" == "help" (
    echo.
    echo "act" to activate virtual environment
    echo "dea" to deactivate virtual environment
    echo "run" to run server
    echo "start" to create and activate virtual environment and install dependencies
    echo "deb" to run server in debug mode
    echo "help" to show this message
    echo.
)
IF "%1" == "" (
    echo "Initializing..."
    timeout /t 2
    start cmd /C "pyxl.bat start > log_start_app.txt 2>&1"
    goto :eof
)