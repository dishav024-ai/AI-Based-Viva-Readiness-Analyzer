@echo off
echo Installing Streamlit and AI...
python -m pip install streamlit google-generativeai speechrecognition pyttsx3 --user
echo.
echo Launching your SDS Dashboard...
python -m streamlit run app.py
pause