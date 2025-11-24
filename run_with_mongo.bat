@echo off
cd /d "%~dp0"
set MONGO_URI=mongodb+srv://raj_db_user:kandukur@videotrackercluster0.eayw3yo.mongodb.net/videotracker?appName=VideoTrackerCluster0
echo Starting Video Tracker with MongoDB...
python app.py
pause
