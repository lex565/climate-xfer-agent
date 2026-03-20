@echo off
cd /d "%~dp0"
echo Starting CLIMATE-XFER Multimodal Agent...
echo.
echo App will open at: http://localhost:8501
echo Press Ctrl+C to stop.
echo.
streamlit run climate_xfer_agent.py
pause
