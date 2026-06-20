@echo off
echo Starting Timmy Training...
python code\train\train_timmy.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Starting Johnny Training...
python code\train\train_johnny.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Starting Spike Training...
python code\train\train_spike.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Starting Ace Training...
python code\train\train_ace.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo All training loops complete!
