REM - This batch file will look in the directory it is in to install the requirements

pip install --no-index --find-links=file://%~dp0 -r requirements.txt