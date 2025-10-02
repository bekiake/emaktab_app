@echo off
echo ===============================================
echo eMaktab Login App - Test Runner
echo ===============================================
echo.

echo Проверка Python...
python --version
if errorlevel 1 (
    echo ОШИБКА: Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

echo.
echo Установка зависимостей...
pip install kivy requests urllib3

echo.
echo Запуск приложения...
cd /d "%~dp0"
python main.py

echo.
echo Приложение завершено.
pause