import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import requests
import csv
import os
import threading
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

kivy.require('2.1.0')


class LoginResult:
    def __init__(self):
        self.successful_logins = []
        self.failed_logins = []
        self.total_users = 0


class EMaktabLoginApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result = LoginResult()
        self.status_label = None
        self.progress_label = None
        
    def build(self):
        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Заголовок
        title_label = Label(
            text='eMaktab Avtomatik Kirish',
            font_size='24sp',
            size_hint_y=None,
            height='50dp',
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title_label)
        
        # Информационный текст
        info_text = (
            "Bu dastur CSV faylidagi barcha foydalanuvchilar uchun "
            "avtomatik ravishda eMaktab tizimiga kirishni amalga oshiradi."
        )
        info_label = Label(
            text=info_text,
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_size='16sp',
            size_hint_y=None,
            height='80dp'
        )
        main_layout.add_widget(info_label)
        
        # Статус метка
        self.status_label = Label(
            text='Tayyor. "Tizimga kirish" tugmasini bosing.',
            font_size='16sp',
            size_hint_y=None,
            height='40dp',
            color=(0, 0.8, 0, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Прогресс метка
        self.progress_label = Label(
            text='',
            font_size='14sp',
            size_hint_y=None,
            height='30dp',
            color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(self.progress_label)
        
        # Кнопка входа
        login_button = Button(
            text='Tizimga kirish',
            font_size='20sp',
            size_hint_y=None,
            height='60dp',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        login_button.bind(on_press=self.start_login_process)
        main_layout.add_widget(login_button)
        
        # Создаем прокручиваемую область для результатов
        scroll = ScrollView()
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def start_login_process(self, instance):
        """Запускает процесс входа в отдельном потоке"""
        instance.disabled = True
        instance.text = 'Jarayon davom etmoqda...'
        instance.background_color = (0.5, 0.5, 0.5, 1)
        
        # Очищаем предыдущие результаты
        self.results_layout.clear_widgets()
        self.result = LoginResult()
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(target=self.perform_login_process)
        thread.daemon = True
        thread.start()
    
    def update_status(self, text, color=(0, 0.8, 0, 1)):
        """Обновляет статус в главном потоке"""
        def update():
            self.status_label.text = text
            self.status_label.color = color
        Clock.schedule_once(lambda dt: update())
    
    def update_progress(self, text):
        """Обновляет прогресс в главном потоке"""
        def update():
            self.progress_label.text = text
        Clock.schedule_once(lambda dt: update())
    
    def add_result(self, text, color=(0, 0, 0, 1)):
        """Добавляет результат в главном потоке"""
        def add():
            result_label = Label(
                text=text,
                font_size='14sp',
                size_hint_y=None,
                height='30dp',
                color=color,
                text_size=(None, None),
                halign='left'
            )
            self.results_layout.add_widget(result_label)
        Clock.schedule_once(lambda dt: add())
    
    def perform_login_process(self):
        """Выполняет процесс входа для всех пользователей"""
        try:
            self.update_status("CSV fayl o'qilmoqda...", (0, 0, 1, 1))
            
            # Читаем пользователей из CSV
            users = self.load_users_from_csv()
            if not users:
                self.update_status("CSV faylda foydalanuvchilar topilmadi!", (1, 0, 0, 1))
                self.reset_button()
                return
            
            self.result.total_users = len(users)
            self.update_status(f"{len(users)} ta foydalanuvchi topildi. Kirish jarayoni boshlanmoqda...", (0, 0, 1, 1))
            
            # Выполняем вход для каждого пользователя
            for i, (username, password) in enumerate(users, 1):
                self.update_progress(f"Jarayon: {i}/{len(users)} - {username}")
                
                success = self.login_user(username, password)
                
                if success:
                    self.result.successful_logins.append(username)
                    self.add_result(f"✅ {username} - Muvaffaqiyatli kirish", (0, 0.8, 0, 1))
                else:
                    self.result.failed_logins.append(username)
                    self.add_result(f"❌ {username} - Kirish xatosi", (1, 0, 0, 1))
            
            # Показываем итоги
            self.show_final_results()
            
        except Exception as e:
            self.update_status(f"Xatolik yuz berdi: {str(e)}", (1, 0, 0, 1))
        finally:
            self.reset_button()
    
    def load_users_from_csv(self):
        """Загружает пользователей из CSV файла"""
        users = []
        csv_path = os.path.join(os.path.dirname(__file__), 'credentials.csv')
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                # Попробуем разные разделители
                content = file.read().strip()
                lines = content.split('\n')
                
                for line in lines:
                    if '\t' in line:
                        parts = line.split('\t')
                    elif ',' in line:
                        parts = line.split(',')
                    else:
                        parts = line.split()
                    
                    if len(parts) >= 2:
                        username = parts[0].strip()
                        password = parts[1].strip()
                        if username and password:
                            users.append((username, password))
                            
        except FileNotFoundError:
            self.update_status("credentials.csv fayli topilmadi!", (1, 0, 0, 1))
        except Exception as e:
            self.update_status(f"CSV fayl o'qishda xatolik: {str(e)}", (1, 0, 0, 1))
        
        return users
    
    def login_user(self, username, password):
        """Выполняет вход для одного пользователя"""
        try:
            # Создаем сессию
            session = requests.Session()
            
            # Настраиваем повторные попытки
            retry_strategy = Retry(
                total=2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            login_url = "https://login.emaktab.uz/"
            
            # Получаем страницу входа
            response = session.get(login_url, timeout=10)
            response.raise_for_status()
            
            # Данные для входа
            login_data = {
                'login': username,
                'password': password
            }
            
            # Заголовки
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': login_url
            }
            
            # Отправляем POST запрос
            login_response = session.post(login_url, data=login_data, headers=headers, 
                                        allow_redirects=True, timeout=10)
            
            # Проверяем успешность входа
            if (login_response.url != login_url and "login" not in login_response.url.lower()) or \
               "userfeed" in login_response.url:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Ошибка входа для {username}: {e}")
            return False
    
    def show_final_results(self):
        """Показывает финальные результаты"""
        successful = len(self.result.successful_logins)
        failed = len(self.result.failed_logins)
        total = self.result.total_users
        
        self.update_status(
            f"Jarayon tugadi! Muvaffaqiyatli: {successful}/{total}, "
            f"Xato: {failed}/{total}", 
            (0, 0.8, 0, 1) if failed == 0 else (1, 0.6, 0, 1)
        )
        
        self.add_result("", (0, 0, 0, 1))  # Пустая строка
        self.add_result("=== YAKUNIY NATIJALAR ===", (0, 0, 1, 1))
        self.add_result(f"Jami foydalanuvchilar: {total}", (0, 0, 0, 1))
        self.add_result(f"Muvaffaqiyatli: {successful}", (0, 0.8, 0, 1))
        self.add_result(f"Xatolik: {failed}", (1, 0, 0, 1))
        
        if successful > 0:
            self.add_result("", (0, 0, 0, 1))
            self.add_result("Muvaffaqiyatli kirganlar:", (0, 0.8, 0, 1))
            for user in self.result.successful_logins:
                self.add_result(f"  • {user}", (0, 0.6, 0, 1))
        
        if failed > 0:
            self.add_result("", (0, 0, 0, 1))
            self.add_result("Xato bilan kirganlar:", (1, 0, 0, 1))
            for user in self.result.failed_logins:
                self.add_result(f"  • {user}", (0.8, 0, 0, 1))
    
    def reset_button(self):
        """Сбрасывает состояние кнопки"""
        def reset():
            # Найдем кнопку в дереве виджетов
            for child in self.root.children:
                if isinstance(child, Button):
                    child.disabled = False
                    child.text = 'Tizimga kirish'
                    child.background_color = (0.2, 0.8, 0.2, 1)
                    break
        Clock.schedule_once(lambda dt: reset())


if __name__ == '__main__':
    EMaktabLoginApp().run()