# eMaktab Auto Login Android приложение

## 📱 Описание
Android приложение для автоматического входа в систему eMaktab для множественных пользователей.

## ✨ Возможности
- 🚀 Простой интерфейс с одной кнопкой "Tizimga kirish"
- 🔄 Автоматический вход для всех пользователей из CSV файла
- 📊 Отображение прогресса и результатов в реальном времени
- 📋 Подробный отчет об успешных и неудачных попытках входа
- ⚡ Многопоточная обработка для быстрой работы
- 🤖 Автоматическая сборка APK через GitHub Actions

## 📁 Структура проекта
```
emaktab_app/
├── .github/
│   └── workflows/
│       └── build-apk.yml     # GitHub Actions workflow
├── main.py                   # Основной файл приложения
├── buildozer.spec           # Конфигурация для сборки APK
├── requirements.txt         # Python зависимости
├── credentials.csv          # Файл с учетными данными (не в git)
├── .gitignore              # Исключения для Git
├── build_instructions.md   # Подробные инструкции по сборке
└── README.md               # Этот файл
```

## 🔧 Быстрая настройка

### 1. Подготовка credentials.csv
Создайте файл `credentials.csv` с логинами и паролями (разделитель - табуляция):
```
username1    password1
username2    password2
username3    password3
```

⚠️ **Важно:** Этот файл не будет загружен в Git по соображениям безопасности!

### 2. Локальное тестирование
```bash
# Установите зависимости
pip install kivy kivymd requests

# Запустите приложение
python main.py
```

## 🚀 Сборка APK через GitHub Actions

### Автоматическая сборка
APK автоматически собирается при:
- Push в ветки `main` или `master`
- Создании Pull Request
- Ручном запуске через GitHub interface

### Как получить APK:

#### Способ 1: Из Actions (Рекомендуется)
1. Перейдите в раздел **Actions** вашего GitHub репозитория
2. Выберите последний успешный build
3. Скачайте артефакт `emaktab-login-app-X` (где X - номер сборки)
4. Разархивируйте и получите APK файл

#### Способ 2: Из Releases (для тегов)
Если вы создаете тег (например, `v1.0`), APK автоматически появится в разделе **Releases**.

### Ручной запуск сборки
1. Откройте вкладку **Actions** в вашем репозитории
2. Выберите workflow "Build APK"
3. Нажмите **Run workflow**
4. Выберите ветку и нажмите **Run workflow**

## 📋 Пошаговая инструкция

### 1. Создание репозитория на GitHub
```bash
# В папке emaktab_app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/emaktab_app.git
git push -u origin main
```

### 2. Настройка credentials.csv
- Создайте файл локально (он не будет загружен в Git)
- Используйте формат: `username[TAB]password`
- Сохраните в кодировке UTF-8

### 3. Запуск сборки
- Push любых изменений запустит автоматическую сборку
- Следите за прогрессом в разделе Actions
- Скачайте готовый APK из артефактов

## 📱 Установка на Android

1. Скачайте APK из GitHub Actions или Releases
2. На Android устройстве разрешите установку из неизвестных источников:
   - Настройки → Безопасность → Неизвестные источники
3. Установите APK файл
4. Добавьте файл `credentials.csv` в папку приложения (если нужно)

## 🔧 Настройка workflow (опционально)

Файл `.github/workflows/build-apk.yml` можно настроить:

```yaml
# Изменить триггеры сборки
on:
  push:
    branches: [ main, develop ]  # Добавить другие ветки
  schedule:
    - cron: '0 2 * * 1'  # Еженедельная сборка

# Изменить версию Python
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # Использовать Python 3.10
```

## 🛠️ Техническая информация

- **Framework:** Kivy 2.1.0
- **HTTP клиент:** requests library
- **Target Android API:** 33 (Android 13)
- **Minimum Android API:** 21 (Android 5.0)
- **Архитектуры:** arm64-v8a, armeabi-v7a

## 🔍 Устранение неполадок

### GitHub Actions не запускается
- Проверьте, что файл находится в `.github/workflows/`
- Убедитесь в правильности YAML синтаксиса
- Проверьте права доступа к репозиторию

### Ошибка сборки APK
- Откройте логи в Actions для детального анализа
- Проверьте `buildozer.spec` конфигурацию
- Убедитесь в актуальности зависимостей в `requirements.txt`

### Ошибка входа в приложении
- Проверьте правильность credentials.csv
- Убедитесь в наличии интернет соединения
- Проверьте доступность сайта eMaktab

## 🔒 Безопасность

- ✅ CSV файл с паролями исключен из Git
- ✅ Никакие учетные данные не хранятся в коде
- ✅ GitHub Actions не имеет доступа к паролям
- ⚠️ Используйте только на доверенных устройствах

## 📄 Лицензия

Проект создан для автоматизации работы с eMaktab. Только для личного использования.

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

**📞 Поддержка:** Если возникли вопросы, создайте Issue в репозитории.