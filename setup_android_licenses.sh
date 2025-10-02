#!/bin/bash
# Скрипт для автоматического принятия лицензий Android SDK

echo "🔧 Настройка Android SDK лицензий..."

# Создаем директорию для Android SDK, если её нет
mkdir -p ~/.android

# Создаем файл конфигурации
echo "count=0" > ~/.android/repositories.cfg

# Автоматически принимаем все лицензии
echo "✅ Принимаем лицензии Android SDK..."

# Список известных лицензий для принятия
echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > ~/.android/licenses/android-sdk-license
echo "84831b9409646a918e30573bab4c9c91346d8abd" > ~/.android/licenses/android-sdk-preview-license
echo "d975f751698a77b662f1254ddbeed3901e976f5a" > ~/.android/licenses/intel-android-extra-license
echo "601085b94cd77f0b54ff86406957099ebe79c4d6" > ~/.android/licenses/android-googletv-license
echo "33b6a2b64607f11b759f320ef9dff4ae5c47d97a" > ~/.android/licenses/google-gdk-license
echo "d056abaabd6c14ce8ff7de8f4b136e01d64e80b7" > ~/.android/licenses/android-sdk-arm-dbt-license

mkdir -p ~/.android/licenses

echo "✅ Лицензии Android SDK настроены!"
echo "Теперь можно запускать buildozer android debug"