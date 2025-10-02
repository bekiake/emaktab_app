@echo off
echo Starting buildozer test...

echo.
echo Installing dependencies...
pip install buildozer cython

echo.
echo Checking buildozer version...
buildozer --version

echo.
echo Checking requirements...
buildozer android requirements

echo.
echo Ready to build APK. Run: buildozer android debug
pause