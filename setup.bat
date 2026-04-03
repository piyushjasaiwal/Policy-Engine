@echo off
echo Creating virtual environment: policy-engine...
python -m venv policy-engine

echo Activating environment...
call .\policy-engine\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Setup complete! To start your app, run: 
echo uvicorn main:app --reload
pause