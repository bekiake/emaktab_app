# eMaktab Auto Login Android приложение

## Описание
Это Android приложение автоматически выполняет вход в систему eMaktab для всех пользователей, указанных в CSV файле.

## Возможности
- ✅ Простой интерфейс с одной кнопкой "Tizimga kirish"
- ✅ Автоматический вход для всех пользователей из CSV файла
- ✅ Отображение прогресса и результатов в реальном времени
- ✅ Подробный отчет об успешных и неудачных попытках входа
- ✅ Многопоточная обработка для быстрой работы

## Структура файлов
```
emaktab_app/
├── main.py              # Основной файл приложения
├── buildozer.spec       # Конфигурация для сборки APK
├── requirements.txt     # Python зависимости
├── credentials.csv      # Файл с учетными данными
├── build_instructions.md # Этот файл с инструкциями
└── README.md           # Описание проекта
```

## Формат CSV файла
Файл `credentials.csv` должен содержать логины и пароли через табуляцию:
```
username1    password1
username2    password2
username3    password3
```

## Сборка APK файла

### Вариант 1: Сборка на Linux (Ubuntu/Debian)

1. **Установка зависимостей:**
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

2. **Установка Buildozer:**
```bash
pip3 install --user buildozer
```

3. **Установка Android SDK (автоматически через buildozer):**
```bash
cd /path/to/emaktab_app/
buildozer android debug
```

### Вариант 2: Сборка через Docker (Windows/Linux/Mac)

1. **Создайте Dockerfile:**
```dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-8-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev

RUN pip3 install buildozer

WORKDIR /app
COPY . /app

CMD ["buildozer", "android", "debug"]
```

2. **Сборка через Docker:**
```bash
# В папке emaktab_app
docker build -t emaktab-builder .
docker run -v ${PWD}:/app emaktab-builder
```

### Вариант 3: Использование GitHub Actions (Рекомендуется)

Создайте файл `.github/workflows/build.yml`:
```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer

    - name: Build APK
      run: |
        buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: emaktab-login-app
        path: bin/*.apk
```

## Быстрый запуск для тестирования

### Тестирование на компьютере (без APK):

1. **Установите Python зависимости:**
```bash
pip install kivy kivymd requests
```

2. **Запустите приложение:**
```bash
cd emaktab_app
python main.py
```

## Готовый APK файл

После успешной сборки APK файл будет находиться в папке:
```
emaktab_app/bin/emaktablogin-1.0-arm64-v8a-debug.apk
```

## Установка на Android

1. Скопируйте APK файл на Android устройство
2. Разрешите установку из неизвестных источников в настройках
3. Откройте APK файл и установите приложение
4. Убедитесь, что файл `credentials.csv` находится в папке приложения

## Использование приложения

1. Откройте приложение "eMaktab Login"
2. Убедитесь, что на устройстве есть интернет
3. Нажмите кнопку "Tizimga kirish"
4. Дождитесь завершения процесса
5. Просмотрите результаты прокруткой вниз

## Решение проблем

### Ошибка "credentials.csv not found"
- Убедитесь, что файл находится в той же папке, что и main.py
- Проверьте формат файла (UTF-8, табуляция как разделитель)

### Ошибки сборки APK
- Убедитесь, что у вас достаточно места на диске (минимум 5GB)
- Проверьте интернет соединение для скачивания Android SDK
- Используйте Linux или Docker для стабильной сборки

### Ошибки входа
- Проверьте правильность логинов и паролей в CSV
- Убедитесь в наличии интернет соединения
- Сайт eMaktab может временно быть недоступен

## Технические детали

- **Framework:** Kivy 2.1.0 (Python GUI framework)
- **HTTP клиент:** requests library
- **Target Android API:** 33 (Android 13)
- **Minimum Android API:** 21 (Android 5.0)
- **Архитектуры:** arm64-v8a, armeabi-v7a

## Безопасность

⚠️ **Важно:** Файл credentials.csv содержит пароли в открытом виде. Убедитесь в безопасности:
- Не передавайте CSV файл третьим лицам
- Удалите CSV после использования, если нужно
- Используйте только на доверенных устройствах

## Лицензия

Этот проект создан для автоматизации входа в eMaktab и предназначен только для личного использования.