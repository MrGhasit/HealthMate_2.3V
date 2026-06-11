import json
import os
import threading
import urllib.request
import urllib.parse
import random
from datetime import datetime, date
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.lang import Builder

import platform
if platform.system() in ('Windows', 'Darwin', 'Linux'):
    Window.size = (400, 700)

# ──────────────────────────────────────────────────
#  ПЕРЕВОДЫ
# ──────────────────────────────────────────────────
TRANSLATIONS = {
    'RU': {
        'app_name': 'HealthMate',
        'subtitle': 'Диетотерапия и ЛФК',
        'start': 'Начать',
        'welcome': 'Добро пожаловать!',
        'login_subtitle': 'Войдите или продолжите как гость',
        'login': 'Войти',
        'register': 'Регистрация',
        'or': '— или —',
        'guest': 'Продолжить как гость',
        'home': 'Главная',
        'diet_tab': 'Режим',
        'chat_tab': 'Чат',
        'weather_tab': 'Погода',
        'profile_tab': 'Профиль',
        'reminders': 'Напоминания',
        'diet': 'Диетотерапия',
        'lfk': 'ЛФК',
        'calendar': 'Расписание',
        'settings': 'Профиль и настройки',
        'weather': 'Погода',
        'community': 'Сообщество',
        'ai_chat': 'Ваш личный помощник',
        'support': 'Техническая поддержка',
        'language': 'Сменить язык',
        'dark_mode': 'Темная тема',
        'notifications': 'Уведомления',
        'notif_screen': 'Уведомления на экране',
        'security': 'БЕЗОПАСНОСТЬ',
        'main_section': 'ОСНОВНОЕ',
        'other': 'ДРУГОЕ',
        'invite': 'Пригласить друзей',
        'delete_profile': 'Удалить профиль',
        'pin': 'Touch ID / PIN-код',
        'set': 'Задать',
        'guest_label': 'Гость',
        'guest_account': 'Гостевой аккаунт',
        'registered': 'Зарегистрирован',
        'find': 'Найти',
        'city_hint': 'Поиск города...',
        'loading': 'Загрузка...',
        'today': 'Сегодня',
        'tomorrow': 'Завтра',
        'after_tomorrow': 'Послезавтра',
        'max': 'Макс',
        'min': 'Мин',
        'precip': 'Осадки',
        'mm': 'мм',
        'send': '>',
        'type_msg': 'Написать сообщение...',
        'close': 'Закрыть',
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'snack': 'Полдник',
        'dinner': 'Ужин',
        'day': 'День',
        'diet_day': 'Диета — день',
        'lfk_day': 'ЛФК — день',
        'schedule_30': 'Расписание 30 дней',
        'click_menu': 'нажмите чтобы увидеть меню',
        'save': 'Сохранить',
        'cancel': 'Отмена',
        'enter_pin': 'Введите 4-значный PIN',
        'need_4': 'Нужно ровно 4 цифры!',
        'pin_title': 'Установить PIN',
        'invite_msg': 'Приложения нет\nв открытом доступе',
        'invitation': 'Приглашение',
        'delete_title': 'Удаление профиля',
        'delete_confirm': 'Вы уверены, что хотите\nудалить профиль?',
        'delete': 'Удалить',
        'info': 'Информация',
        'ok': 'OK',
        'city_not_found': 'Город не найден',
        'conn_error': 'Ошибка соединения',
        'you': 'Вы',
        'reg_email': 'Email',
        'reg_password': 'Пароль',
        'reg_confirm': 'Подтвердите пароль',
        'reg_btn': 'Зарегистрироваться',
        'back_btn': '< Назад',
        'email_error': 'Неверный формат email',
        'pass_error': 'Пароль слишком короткий (мин. 6 символов)',
        'confirm_error': 'Пароли не совпадают',
        'register_screen': 'Создать аккаунт',
        'pin_unavailable': 'Touch ID / PIN будет доступен\nв следующем обновлении',
        'lang_pick_title': 'Выберите язык',
        'messages': 'Сообщения',
        'select_chat': 'Выберите чат',
        'community_desc': 'Общайтесь с участниками',
        'ai_desc': 'AI советник по здоровью',
        'support_desc': 'Помощь по приложению',
        'ask_question': 'Задайте вопрос...',
        'describe_problem': 'Опишите проблему...',
        'day_regime': 'Режим дня',
        'tap_block': 'Нажмите на блок — меню и упражнения',
        'meal_time': 'Время приема пищи',
        'walk_desc': 'Ходьба 20-30 мин',
        'light_snack': 'Легкий перекус',
        'light_dinner': 'Легкий ужин',
        'morning_ex_desc': 'ЛФК — утренний комплекс',
        'evening_ex': 'Вечерняя гимнастика',
        'stretch_relax': 'Растяжка и расслабление',
        'sleep_time': 'Время сна',
        'rest_desc': 'Время отдыха',
        'news': 'НОВОСТИ',
        'soon_market': 'Скоро в Play Market и App Store!',
        'preparing': 'Готовим к публикации!',
        'together': 'Вместе к лучшему!',
        'every_day': 'Каждый день — шаг к здоровью!',
        'schedule_header': 'Расписание 30 дней',
        'breakfast_col': 'Завтрак',
        'lfk_col': 'ЛФК',
        'weather_kz': 'Погода Казахстана',
        'profile_settings': 'Профиль и настройки',
        'personal_data': 'Личные данные никто не видит.',
        'version': 'HealthMate v2.3',
        'login_later': 'Вход будет доступен в следующем обновлении',
        'diet_today': 'Диетотерапия',
        'lfk_today': 'ЛФК',
        'reminder': 'Режим дня',
        'ai_hello': 'Привет! Задайте любой вопрос о здоровье!',
        'support_hello': 'Здравствуйте! Чем могу помочь?',
        'ai_label': 'HealthMate AI',
        'support_label': 'Поддержка HealthMate',
        'trainer_label': 'Тренер Алина',
        'trainer_hello': 'Привет! Добро пожаловать в чат!',
        'svetlana_msg': 'Сегодня выполнила всё ЛФК!',
        'today_menu': 'Меню на сегодня:',
        'exercises': 'Упражнения:',
        'program_day': 'День программы',
        'from_30': 'из 30',
    },
    'EN': {
        'app_name': 'HealthMate',
        'subtitle': 'Diet Therapy & Physical Therapy',
        'start': 'Start',
        'welcome': 'Welcome!',
        'login_subtitle': 'Sign in or continue as guest',
        'login': 'Sign In',
        'register': 'Register',
        'or': '— or —',
        'guest': 'Continue as Guest',
        'home': 'Home',
        'diet_tab': 'Diet',
        'chat_tab': 'Chat',
        'weather_tab': 'Weather',
        'profile_tab': 'Profile',
        'reminders': 'Reminders',
        'diet': 'Diet Therapy',
        'lfk': 'Physical Therapy',
        'calendar': 'Schedule',
        'settings': 'Profile & Settings',
        'weather': 'Weather',
        'community': 'Community',
        'ai_chat': 'Your Personal Assistant',
        'support': 'Technical Support',
        'language': 'Change Language',
        'dark_mode': 'Dark Mode',
        'notifications': 'Notifications',
        'notif_screen': 'On-screen Notifications',
        'security': 'SECURITY',
        'main_section': 'GENERAL',
        'other': 'OTHER',
        'invite': 'Invite Friends',
        'delete_profile': 'Delete Profile',
        'pin': 'Touch ID / PIN',
        'set': 'Set',
        'guest_label': 'Guest',
        'guest_account': 'Guest Account',
        'registered': 'Registered',
        'find': 'Find',
        'city_hint': 'Search city...',
        'loading': 'Loading...',
        'today': 'Today',
        'tomorrow': 'Tomorrow',
        'after_tomorrow': 'Day after tomorrow',
        'max': 'Max',
        'min': 'Min',
        'precip': 'Precip',
        'mm': 'mm',
        'send': '>',
        'type_msg': 'Write a message...',
        'close': 'Close',
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'snack': 'Snack',
        'dinner': 'Dinner',
        'day': 'Day',
        'diet_day': 'Diet — day',
        'lfk_day': 'PT — day',
        'schedule_30': '30-Day Schedule',
        'click_menu': 'tap to see menu',
        'save': 'Save',
        'cancel': 'Cancel',
        'enter_pin': 'Enter 4-digit PIN',
        'need_4': 'Must be exactly 4 digits!',
        'pin_title': 'Set PIN',
        'invite_msg': 'App not\npublicly available',
        'invitation': 'Invitation',
        'delete_title': 'Delete Profile',
        'delete_confirm': 'Are you sure you want\nto delete your profile?',
        'delete': 'Delete',
        'info': 'Information',
        'ok': 'OK',
        'city_not_found': 'City not found',
        'conn_error': 'Connection error',
        'you': 'You',
        'reg_email': 'Email',
        'reg_password': 'Password',
        'reg_confirm': 'Confirm password',
        'reg_btn': 'Create Account',
        'back_btn': '< Back',
        'email_error': 'Invalid email format',
        'pass_error': 'Password too short (min. 6 characters)',
        'confirm_error': 'Passwords do not match',
        'register_screen': 'Create Account',
        'pin_unavailable': 'Touch ID / PIN will be available\nin the next update',
        'lang_pick_title': 'Select Language',
        'messages': 'Messages',
        'select_chat': 'Select a chat',
        'community_desc': 'Chat with members',
        'ai_desc': 'AI health advisor',
        'support_desc': 'App help & support',
        'ask_question': 'Ask a question...',
        'describe_problem': 'Describe your issue...',
        'day_regime': 'Daily Routine',
        'tap_block': 'Tap a block — menu and exercises',
        'meal_time': 'Meal time',
        'walk_desc': 'Walk 20-30 min',
        'light_snack': 'Light snack',
        'light_dinner': 'Light dinner',
        'morning_ex_desc': 'PT — morning session',
        'evening_ex': 'Evening Exercise',
        'stretch_relax': 'Stretching and relaxation',
        'sleep_time': 'Bedtime',
        'rest_desc': 'Rest time',
        'news': 'NEWS',
        'soon_market': 'Coming to Play Market and App Store!',
        'preparing': 'Getting ready for launch!',
        'together': 'Better together!',
        'every_day': 'Every day is a step toward health!',
        'schedule_header': '30-Day Schedule',
        'breakfast_col': 'Breakfast',
        'lfk_col': 'PT',
        'weather_kz': 'Kazakhstan Weather',
        'profile_settings': 'Profile & Settings',
        'personal_data': 'Your data is private.',
        'version': 'HealthMate v2.3',
        'login_later': 'Login will be available in the next update',
        'diet_today': 'Diet Therapy',
        'lfk_today': 'Physical Therapy',
        'reminder': 'Daily Routine',
        'ai_hello': 'Hi! Ask any question about your health!',
        'support_hello': 'Hello! How can I help you?',
        'ai_label': 'HealthMate AI',
        'support_label': 'HealthMate Support',
        'trainer_label': 'Coach Alina',
        'trainer_hello': 'Hello! Welcome to the chat!',
        'svetlana_msg': 'Completed all PT exercises today!',
        'today_menu': "Today's menu:",
        'exercises': 'Exercises:',
        'program_day': 'Program day',
        'from_30': 'of 30',
    },
    'KZ': {
        'app_name': 'HealthMate',
        'subtitle': 'Диеттерапия және ЕДШ',
        'start': 'Бастау',
        'welcome': 'Қош келдіңіз!',
        'login_subtitle': 'Кіріңіз немесе қонақ ретінде жалғастырыңыз',
        'login': 'Кіру',
        'register': 'Тіркелу',
        'or': '— немесе —',
        'guest': 'Қонақ ретінде жалғастыру',
        'home': 'Басты',
        'diet_tab': 'Режим',
        'chat_tab': 'Чат',
        'weather_tab': 'Ауа-райы',
        'profile_tab': 'Профиль',
        'reminders': 'Еске салғыштар',
        'diet': 'Диеттерапия',
        'lfk': 'ЕДШ',
        'calendar': 'Кесте',
        'settings': 'Профиль және параметрлер',
        'weather': 'Ауа-райы',
        'community': 'Қауымдастық',
        'ai_chat': 'Жеке көмекшіңіз',
        'support': 'Техникалық қолдау',
        'language': 'Тілді өзгерту',
        'dark_mode': 'Күңгірт тақырып',
        'notifications': 'Хабарландырулар',
        'notif_screen': 'Экрандағы хабарландырулар',
        'security': 'ҚАУІПСІЗДІК',
        'main_section': 'НЕГІЗГІ',
        'other': 'БАСҚА',
        'invite': 'Достарды шақыру',
        'delete_profile': 'Профильді жою',
        'pin': 'Touch ID / PIN-код',
        'set': 'Орнату',
        'guest_label': 'Қонақ',
        'guest_account': 'Қонақ аккаунты',
        'registered': 'Тіркелген',
        'find': 'Іздеу',
        'city_hint': 'Қала іздеу...',
        'loading': 'Жүктелуде...',
        'today': 'Бүгін',
        'tomorrow': 'Ертең',
        'after_tomorrow': 'Арғы күн',
        'max': 'Макс',
        'min': 'Мин',
        'precip': 'Жауын-шашын',
        'mm': 'мм',
        'send': '>',
        'type_msg': 'Хабар жазыңыз...',
        'close': 'Жабу',
        'breakfast': 'Таңғы ас',
        'lunch': 'Түскі ас',
        'snack': 'Аралық тамақ',
        'dinner': 'Кешкі ас',
        'day': 'Күн',
        'diet_day': 'Диета — күн',
        'lfk_day': 'ЕДШ — күн',
        'schedule_30': '30 күндік кесте',
        'click_menu': 'мәзірді көру үшін басыңыз',
        'save': 'Сақтау',
        'cancel': 'Болдырмау',
        'enter_pin': '4 санды PIN енгізіңіз',
        'need_4': 'Дәл 4 сан болуы керек!',
        'pin_title': 'PIN орнату',
        'invite_msg': 'Қолданба\nашық қолжетімді емес',
        'invitation': 'Шақыру',
        'delete_title': 'Профильді жою',
        'delete_confirm': 'Профильді жойғыңыз\nкелетіні сенімдісіз бе?',
        'delete': 'Жою',
        'info': 'Ақпарат',
        'ok': 'OK',
        'city_not_found': 'Қала табылмады',
        'conn_error': 'Қосылу қатесі',
        'you': 'Сіз',
        'reg_email': 'Email',
        'reg_password': 'Құпиясөз',
        'reg_confirm': 'Құпиясөзді растаңыз',
        'reg_btn': 'Тіркелу',
        'back_btn': '< Артқа',
        'email_error': 'Email форматы дұрыс емес',
        'pass_error': 'Құпиясөз тым қысқа (мин. 6 таңба)',
        'confirm_error': 'Құпиясөздер сәйкес келмейді',
        'register_screen': 'Аккаунт жасау',
        'pin_unavailable': 'Touch ID / PIN келесі жаңартуда\nқолжетімді болады',
        'lang_pick_title': 'Тілді таңдаңыз',
        'messages': 'Хабарлар',
        'select_chat': 'Чат таңдаңыз',
        'community_desc': 'Қатысушылармен сөйлесіңіз',
        'ai_desc': 'AI денсаулық кеңесшісі',
        'support_desc': 'Қолданба бойынша көмек',
        'ask_question': 'Сұрақ қойыңыз...',
        'describe_problem': 'Мәселені сипаттаңыз...',
        'day_regime': 'Күн режимі',
        'tap_block': 'Блокты басыңыз — мәзір және жаттығулар',
        'meal_time': 'Тамақтану уақыты',
        'walk_desc': 'Жаяу жүру 20-30 мин',
        'light_snack': 'Жеңіл тағам',
        'light_dinner': 'Жеңіл кешкі ас',
        'morning_ex_desc': 'ЕДШ — таңғы кешен',
        'evening_ex': 'Кешкі гимнастика',
        'stretch_relax': 'Созылу және демалу',
        'sleep_time': 'Ұйқы уақыты',
        'rest_desc': 'Демалыс уақыты',
        'news': 'ЖАҢАЛЫҚТАР',
        'soon_market': 'Play Market және App Store-да жақында!',
        'preparing': 'Жарияланымға дайындалуда!',
        'together': 'Бірге жақсыға!',
        'every_day': 'Әр күн — денсаулыққа қадам!',
        'schedule_header': '30 күндік кесте',
        'breakfast_col': 'Таңғы ас',
        'lfk_col': 'ЕДШ',
        'weather_kz': 'Қазақстан ауа-райы',
        'profile_settings': 'Профиль және параметрлер',
        'personal_data': 'Жеке деректеріңіз жасырын.',
        'version': 'HealthMate v2.3',
        'login_later': 'Кіру келесі жаңартуда қолжетімді болады',
        'diet_today': 'Диеттерапия',
        'lfk_today': 'ЕДШ',
        'reminder': 'Күн режимі',
        'ai_hello': 'Сәлем! Денсаулық туралы кез келген сұрақ қойыңыз!',
        'support_hello': 'Сәлем! Қалай көмектесе аламын?',
        'ai_label': 'HealthMate AI',
        'support_label': 'HealthMate қолдауы',
        'trainer_label': 'Жаттықтырушы Алина',
        'trainer_hello': 'Сәлем! Чатқа қош келдіңіз!',
        'svetlana_msg': 'Бүгін барлық ЕДШ жаттығуларын орындадым!',
        'today_menu': 'Бүгінгі мәзір:',
        'exercises': 'Жаттығулар:',
        'program_day': 'Бағдарлама күні',
        'from_30': '30-дан',
    }
}

current_lang = ['RU']

def t(key):
    lang = current_lang[0]
    return TRANSLATIONS.get(lang, TRANSLATIONS['RU']).get(key, TRANSLATIONS['RU'].get(key, key))

# ──────────────────────────────────────────────────
#  ТЕМА
# ──────────────────────────────────────────────────
def apply_theme(dark: bool):
    if dark:
        Window.clearcolor = get_color_from_hex('#0F1923FF')
    else:
        Window.clearcolor = get_color_from_hex('#F0F4F8FF')

# ──────────────────────────────────────────────────
#  ГОРОДА КАЗАХСТАНА
# ──────────────────────────────────────────────────
KZ_CITIES = [
    'Алматы', 'Астана', 'Шымкент', 'Актобе', 'Тараз',
    'Павлодар', 'Усть-Каменогорск', 'Семей', 'Атырау', 'Костанай',
    'Кызылорда', 'Уральск', 'Петропавловск', 'Актау', 'Темиртау',
    'Туркестан', 'Балхаш', 'Жезказган', 'Экибастуз', 'Рудный',
    'Жанаозен', 'Талдыкорган', 'Кокшетау', 'Щучинск', 'Жаркент',
    'Риддер', 'Степногорск', 'Байконыр', 'Аральск', 'Каратау',
]

DIET_PLAN = [
    {"breakfast":"Овсяная каша с яблоком","lunch":"Куриный суп с овощами","snack":"Кефир + груша","dinner":"Куриная грудка + брокколи"},
    {"breakfast":"Творог с медом и орехами","lunch":"Суп-пюре из тыквы + индейка","snack":"Запеченное яблоко","dinner":"Рыба на пару + бурый рис"},
    {"breakfast":"Яйца всмятку + тост","lunch":"Борщ без зажарки + курица","snack":"Смузи банан+кефир","dinner":"Тушеные овощи + индейка"},
    {"breakfast":"Манная каша + ягоды","lunch":"Щи из капусты + говядина","snack":"Кефир + хлебец","dinner":"Запеченный минтай + гречка"},
    {"breakfast":"Гречневая каша молочная","lunch":"Уха из горбуши","snack":"Творог с ягодами","dinner":"Паровые котлеты + цветная капуста"},
    {"breakfast":"Омлет 2 яйца + огурец","lunch":"Рисовый суп с курицей","snack":"Банан + орехи","dinner":"Куриное филе + картофель"},
    {"breakfast":"Пшённая каша с тыквой","lunch":"Суп-минестроне + телятина","snack":"Натуральный йогурт","dinner":"Треска запеченная + горошек"},
    {"breakfast":"Мюсли без сахара + молоко","lunch":"Гороховый суп + котлета","snack":"Кефир + хлебец","dinner":"Тушеная капуста + куриное филе"},
    {"breakfast":"Творожная запеканка","lunch":"Куриный бульон + вермишель","snack":"Яблоко + миндаль","dinner":"Запеченный лосось + рис"},
    {"breakfast":"Геркулес с изюмом","lunch":"Суп из чечевицы + индейка","snack":"Смузи шпинат+яблоко","dinner":"Паровые рыбные котлеты + брокколи"},
    {"breakfast":"Яичница + помидор + тост","lunch":"Суп с фрикадельками","snack":"Творог с медом","dinner":"Тушеная говядина + гречка"},
    {"breakfast":"Рисовая каша молочная","lunch":"Окрошка на кефире","snack":"Грейпфрут + кешью","dinner":"Запеченная треска + бурый рис"},
    {"breakfast":"Овсянка с бананом","lunch":"Суп-лапша куриная","snack":"Кефир + хлебец","dinner":"Куриное филе с грибами + пшено"},
    {"breakfast":"Гречка + яйцо","lunch":"Рассольник + говядина","snack":"Натуральный йогурт + груша","dinner":"Паровой хек + цветная капуста"},
    {"breakfast":"Творог + банан + корица","lunch":"Суп из кабачков + котлета","snack":"Яблоко + фундук","dinner":"Запеченная индейка + картофель"},
    {"breakfast":"Пшённая каша молочная","lunch":"Борщ постный + курица","snack":"Смузи клубника+кефир","dinner":"Запеченный минтай + гречка"},
    {"breakfast":"Омлет с овощами","lunch":"Уха из трески","snack":"Кефир + хлебец","dinner":"Тушеные кабачки + индейка + рис"},
    {"breakfast":"Геркулес с черникой","lunch":"Суп гречневый с курицей","snack":"Банан + миндаль","dinner":"Паровые котлеты говяжьи + брокколи"},
    {"breakfast":"Яйца всмятку + тост","lunch":"Суп-пюре из горошка","snack":"Творог с киви","dinner":"Запеченный лосось + картофель"},
    {"breakfast":"Манная каша молочная","lunch":"Щи с грибами + курица","snack":"Кефир + груша","dinner":"Тушеная рыба с морковью + пшено"},
    {"breakfast":"Гречка молочная","lunch":"Рисовый суп с курицей","snack":"Смузи шпинат+банан","dinner":"Куриное филе запеченное + гречка"},
    {"breakfast":"Творожная запеканка","lunch":"Суп с чечевицей + котлета","snack":"Запеченное яблоко + орехи","dinner":"Треска на пару + бурый рис"},
    {"breakfast":"Овсянка с яблоком","lunch":"Борщ с телятиной","snack":"Натуральный йогурт + киви","dinner":"Запеченная индейка + брокколи"},
    {"breakfast":"Мюсли + молоко","lunch":"Куриный суп с рисом","snack":"Кефир + хлебец","dinner":"Паровой минтай + цветная капуста"},
    {"breakfast":"Яичница + помидор + тост","lunch":"Суп с фрикадельками","snack":"Смузи малина+творог","dinner":"Тушеная говядина с овощами + гречка"},
    {"breakfast":"Пшённая каша с тыквой","lunch":"Гороховый суп + курица","snack":"Банан + миндаль","dinner":"Запеченный хек с морковью + рис"},
    {"breakfast":"Геркулес с изюмом","lunch":"Суп-лапша с индейкой","snack":"Творог с медом + груша","dinner":"Куриное филе с кабачком + гречка"},
    {"breakfast":"Омлет + зелень + огурец","lunch":"Рассольник + телятина","snack":"Кефир + хлебец","dinner":"Лосось запеченный + брокколи"},
    {"breakfast":"Гречка + яйцо вкрутую","lunch":"Суп из кабачков с рисом + котлета","snack":"Смузи яблоко+кефир","dinner":"Запеченная индейка + пшено"},
    {"breakfast":"Творог с ягодами","lunch":"Борщ с говядиной","snack":"Натуральный йогурт + киви","dinner":"Рыба на пару + гречка + салат"},
]

LFK_PLAN = [
    {"title":"Дыхательная гимнастика","exercises":["Диафрагмальное дыхание — 10 мин","Медленные вдохи через нос — 15 раз","Выдох трубочкой — 15 раз","Подъём рук на вдохе лёжа — 10 раз"]},
    {"title":"Суставная разминка","exercises":["Вращение кистями — 10 раз","Вращение локтями — 10 раз","Вращение плечами — 10 раз","Наклоны головы — 8 раз"]},
    {"title":"Упражнения лёжа","exercises":["Сжимание пальцев — 15 раз","Подъём ноги лёжа — 10 раз","Велосипед лёжа — 30 сек","Мост (ягодицы вверх) — 10 раз"]},
    {"title":"Упражнения сидя","exercises":["Подъём на носки сидя — 15 раз","Разгибание колена — 10 раз","Наклоны туловища — 8 раз","Повороты корпуса — 8 раз"]},
    {"title":"Лёгкая растяжка","exercises":["Растяжка плеч — 2 мин","Наклон к ногам сидя — 10 раз","Растяжка икр — 1 мин","Кошка-корова — 10 раз"]},
    {"title":"Дыхание и релаксация","exercises":["Брюшное дыхание — 5 мин","Мышечная релаксация — 10 мин","Медитация лёжа — 5 мин"]},
    {"title":"Ходьба и равновесие","exercises":["Медленная ходьба — 10 мин","Стойка на одной ноге — 30 сек","Ходьба пятками — 2 мин","Ходьба на носках — 2 мин"]},
    {"title":"Упражнения для рук","exercises":["Сжимание мячика — 15 раз","Подъём рук вперёд — 10 раз","Разведение рук — 10 раз","Растяжка пальцев — 2 мин"]},
    {"title":"Укрепление спины","exercises":["Лодочка лёжа — 10 раз","Кошка-корова — 10 раз","Боковые наклоны — 10 раз","Повороты шеи — 8 раз"]},
    {"title":"Упражнения для ног","exercises":["Подъём ног лёжа — 10 раз","Сгибание колен стоя — 15 раз","Отведение ноги — 10 раз","Тяга пятки к ягодице — 10 раз"]},
    {"title":"Координация","exercises":["Ходьба по линии — 2 мин","Перешагивание — 5 мин","Марш на месте — 3 мин","Восьмёрки ногой — 10 раз"]},
    {"title":"Укрепление пресса","exercises":["Подъём головы лёжа — 10 раз","Втягивание живота — 10 раз","Подъём согнутых ног — 10 раз","Боковые скручивания — 8 раз"]},
    {"title":"Дыхание и суставы","exercises":["Полное дыхание — 5 мин","Вращение голеностопом — 10 раз","Вращение тазом — 10 раз","Потягивание — 2 мин"]},
    {"title":"Активный день","exercises":["Ходьба на улице — 20 мин","Приседания с опорой — 10 раз","Подъём на носки — 15 раз","Растяжка — 5 мин"]},
    {"title":"День восстановления","exercises":["Массаж кистей — 5 мин","Тёплая ванна для ног — 10 мин","Глубокое дыхание — 5 мин","Растяжка перед сном — 5 мин"]},
    {"title":"Равновесие","exercises":["Стойка у стены на носках — 1 мин","Перекаты с пятки на носок — 15 раз","Покачивание стоя — 2 мин","Ходьба с поворотами — 5 мин"]},
    {"title":"Комплекс для плеч","exercises":["Пожимание плечами — 15 раз","Вращение плечами — 10 раз","Разведение лопаток — 10 раз","Наклоны головы — 8 раз"]},
    {"title":"Лёжа и дыхание","exercises":["Мост — 10 раз","Велосипед — 30 сек","Дыхательные упражнения — 5 мин","Расслабление тела — 5 мин"]},
    {"title":"Мягкая нагрузка","exercises":["Ходьба — 15 мин","Подъём на носки — 15 раз","Марш с подъёмом колен — 2 мин","Растяжка икр — 2 мин"]},
    {"title":"Укрепление кора","exercises":["Планка на локтях — 20 сек","Боковая планка — 15 сек","Рука+нога противоположные — 10 раз","Скручивания мягкие — 10 раз"]},
    {"title":"День растяжки","exercises":["Растяжка тела лёжа — 5 мин","Растяжка бёдер — 2 мин","Растяжка плеч — 2 мин","Поза ребёнка — 3 мин"]},
    {"title":"Активация","exercises":["Мягкие прыжки — 30 сек","Приседания — 10 раз","Выпады вперёд — 8 раз","Ходьба на месте — 5 мин"]},
    {"title":"Суставы и дыхание","exercises":["Вращение суставов — 10 мин","Полное дыхание — 5 мин","Потягивание — 2 мин"]},
    {"title":"С эспандером","exercises":["Сгибание руки — 10 раз","Разгибание — 10 раз","Подъём ноги — 10 раз","Растяжка — 2 мин"]},
    {"title":"Осанка и дыхание","exercises":["Дыхание у стены — 5 мин","Прогиб назад — 10 раз","Стойка с ровной спиной — 3 мин","Растяжка груди — 2 мин"]},
    {"title":"Лёгкое кардио","exercises":["Ходьба — 25 мин","Подъём по ступеням — 5 мин","Растяжка после ходьбы — 5 мин"]},
    {"title":"Полное расслабление","exercises":["Глубокое дыхание — 10 мин","Шавасана — 10 мин","Самомассаж — 10 мин"]},
    {"title":"Укрепление ног","exercises":["Приседания у стены — 10 раз","Шаги в сторону — 15 раз","Подъём на носки — 20 раз","Растяжка бёдер — 2 мин"]},
    {"title":"Руки и плечи","exercises":["Отжимания от стены — 10 раз","Разведение рук — 10 раз","Подъём рук вперёд — 10 раз","Растяжка плеч — 3 мин"]},
    {"title":"Итоговая тренировка","exercises":["Дыхательная разминка — 3 мин","Суставная гимнастика — 5 мин","Ходьба — 15 мин","Упражнения на кор — 5 мин","Растяжка тела — 5 мин","Релаксация — 5 мин"]},
]

store = JsonStore('healthmate_data.json')

def get_setting(key, default=None):
    try:
        if store.exists('settings'):
            return store.get('settings').get(key, default)
    except Exception:
        pass
    return default

def set_setting(key, value):
    try:
        d = dict(store.get('settings')) if store.exists('settings') else {}
        d[key] = value
        store.put('settings', **d)
    except Exception:
        pass

def get_day_index():
    return (date.today().timetuple().tm_yday - 1) % 30

def get_lfk_day_for_user(is_guest):
    if is_guest:
        return 0
    saved = get_setting('lfk_day_index', None)
    if saved is None:
        return get_day_index()
    return saved % 30

def show_popup(title, text, btn_text='OK'):
    content = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(10))
    content.add_widget(Label(
        text=text, halign='center', valign='middle',
        color=get_color_from_hex('#FFFFFF'),
        font_size=dp(14), text_size=(dp(260), None)
    ))
    btn = Button(
        text=btn_text, size_hint_y=None, height=dp(44),
        background_normal='', background_color=get_color_from_hex('#6BCB77'),
        color=get_color_from_hex('#FFFFFF'), font_size=dp(15)
    )
    content.add_widget(btn)
    popup = Popup(
        title=title, content=content,
        size_hint=(0.85, None), height=dp(220),
        background_color=get_color_from_hex('#1E2E3E'),
        title_color=get_color_from_hex('#FFD93D'),
        separator_color=get_color_from_hex('#6BCB77')
    )
    btn.bind(on_release=popup.dismiss)
    popup.open()
    return popup


# ──────────────────────────────────────────────────
#  ЭКРАНЫ
# ──────────────────────────────────────────────────
class MainScreen(Screen):
    date_text = StringProperty('')
    def on_enter(self):
        now = datetime.now()
        months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря']
        self.date_text = f"{now.day} {months[now.month-1]} {now.year}"


class LoginScreen(Screen):
    def show_register(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'register'
    def show_unavailable(self):
        show_popup(t('info'), t('login_later'))
    def guest_login(self):
        set_setting('is_guest', True)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'app_screen'


class RegisterScreen(Screen):
    email_error = StringProperty('')
    pass_error = StringProperty('')
    confirm_error = StringProperty('')

    def try_register(self, email, password, confirm):
        import re
        has_error = False
        if not re.match(r'^[^\@\s]+@[^\@\s]+\.[^\@\s]+$', email):
            self.email_error = t('email_error')
            has_error = True
        else:
            self.email_error = ''
        if len(password) < 6:
            self.pass_error = t('pass_error')
            has_error = True
        else:
            self.pass_error = ''
        if password != confirm and not has_error:
            self.confirm_error = t('confirm_error')
            has_error = True
        elif password == confirm:
            self.confirm_error = ''
        if not has_error:
            self.email_error = 'Эта почта не найдена в системе'

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


class AppScreen(Screen):
    date_text = StringProperty('')

    def on_enter(self):
        now = datetime.now()
        months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря']
        self.date_text = f"{now.day} {months[now.month-1]} {now.year}"

    def open_diet_today(self):
        idx = get_day_index()
        day = DIET_PLAN[idx]
        content = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(14), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        for key_lbl, key_data in [(t('breakfast'),'breakfast'),(t('lunch'),'lunch'),(t('snack'),'snack'),(t('dinner'),'dinner')]:
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(74), padding=[dp(12),dp(8)], spacing=dp(4))
            with item.canvas.before:
                Color(rgba=get_color_from_hex('#1B4D3E'))
                item._bg = RoundedRectangle(size=item.size, pos=item.pos, radius=[dp(10)])
            item.bind(size=lambda w,v: setattr(w._bg,'size',v))
            item.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            item.add_widget(Label(text=key_lbl, font_size=dp(12), bold=True, color=get_color_from_hex('#6BCB77'), halign='left', text_size=(dp(280),None), size_hint_y=None, height=dp(20)))
            item.add_widget(Label(text=day[key_data], font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(280),None), size_hint_y=None, height=dp(38)))
            box.add_widget(item)
        content.add_widget(box)
        close_btn = Button(text=t('close'), size_hint_y=None, height=dp(44), background_normal='', background_color=get_color_from_hex('#6BCB77'))
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)
        popup = Popup(title=f'{t("diet_day")} {idx+1}', content=wrap, size_hint=(0.93,0.82),
                      background_color=get_color_from_hex('#1A2535'), title_color=get_color_from_hex('#FFD93D'), separator_color=get_color_from_hex('#6BCB77'))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def open_lfk_today(self):
        is_guest = get_setting('is_guest', True)
        idx = get_lfk_day_for_user(is_guest)
        day = LFK_PLAN[idx]
        content = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(14), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(Label(text=day['title'], font_size=dp(15), bold=True, color=get_color_from_hex('#FFD93D'), halign='left', text_size=(dp(280),None), size_hint_y=None, height=dp(30)))
        for ex in day['exercises']:
            box.add_widget(Label(text=f"  • {ex}", font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(280),None), size_hint_y=None, height=dp(32)))
        content.add_widget(box)
        close_btn = Button(text=t('close'), size_hint_y=None, height=dp(44), background_normal='', background_color=get_color_from_hex('#6BCB77'))
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)
        popup = Popup(title=f'{t("lfk_day")} {idx+1}', content=wrap, size_hint=(0.93,0.75),
                      background_color=get_color_from_hex('#1A2535'), title_color=get_color_from_hex('#FFD93D'), separator_color=get_color_from_hex('#6BCB77'))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class CalendarScreen(Screen):
    def on_enter(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()
        today_idx = get_day_index()
        for i in range(30):
            diet = DIET_PLAN[i]
            lfk  = LFK_PLAN[i]
            is_today = (i == today_idx)
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(54), spacing=dp(6), padding=[dp(10),dp(4)])
            with row.canvas.before:
                Color(rgba=get_color_from_hex('#1B4D3E' if is_today else '#1E2E3E'))
                row._bg = RoundedRectangle(size=row.size, pos=row.pos, radius=[dp(8)])
            row.bind(size=lambda w,v: setattr(w._bg,'size',v))
            row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            prefix = ">> " if is_today else ""
            row.add_widget(Label(text=f"{prefix}{t('day')} {i+1}", font_size=dp(12), bold=is_today, color=get_color_from_hex('#FFD93D' if is_today else '#FFFFFF'), size_hint_x=0.22, halign='left', text_size=(dp(80),None)))
            row.add_widget(Label(text=diet['breakfast'][:26], font_size=dp(11), color=get_color_from_hex('#A8C5DA'), size_hint_x=0.45, halign='left', text_size=(dp(160),None)))
            row.add_widget(Label(text=lfk['title'][:18], font_size=dp(11), color=get_color_from_hex('#D8A8F0'), size_hint_x=0.33, halign='right', text_size=(dp(110),None)))
            grid.add_widget(row)


class ReminderScreen(Screen):
    TIME_BLOCKS = {
        'breakfast': {'time':'08:00','title':'Завтрак','food_key':'breakfast','exercises':['Выпейте стакан воды сразу после пробуждения','Легкая растяжка — 5 мин','Дыхательная гимнастика — 3 мин']},
        'morning_ex': {'time':'10:00','title':'Утренние упражнения','food_key':None,'exercises':None},
        'lunch': {'time':'12:00','title':'Обед','food_key':'lunch','exercises':['После обеда: спокойная прогулка 10-15 мин','Не ложитесь сразу — посидите спокойно','Выпейте воду через 30 минут после еды']},
        'walk': {'time':'14:00','title':'Прогулка','food_key':None,'exercises':['Спокойная ходьба на свежем воздухе — 20-30 мин','Дыхание через нос, ритмичный шаг','Избегайте резкого темпа и подъёмов','Лёгкая разминка суставов перед выходом']},
        'snack': {'time':'16:00','title':'Полдник','food_key':'snack','exercises':['Лёгкие упражнения сидя — 5 мин','Гимнастика для рук и плеч — 3 мин','Дыхательные упражнения — 2 мин']},
        'dinner': {'time':'18:00','title':'Ужин','food_key':'dinner','exercises':['Лёгкая растяжка после ужина — 5 мин','Небольшая прогулка по квартире','Стакан воды или травяного чая']},
        'evening_ex': {'time':'20:00','title':'Вечерняя гимнастика','food_key':None,'exercises':['Поза ребёнка — 2 мин','Растяжка спины лёжа — 3 мин','Медленное дыхание животом — 5 мин','Мышечная релаксация — 5 мин']},
        'sleep': {'time':'22:00','title':'Время сна','food_key':None,'exercises':['Уберите телефон и выключите яркий свет','Проветрите комнату 10 мин','Лягте удобно, расслабьте тело','Дышите медленно: вдох 4с — выдох 6с']},
    }

    def show_time_detail(self, block_key):
        block = self.TIME_BLOCKS.get(block_key)
        if not block:
            return
        idx = get_day_index()
        diet_day = DIET_PLAN[idx]
        lfk_day  = LFK_PLAN[idx]
        content = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(Label(text=f"{block['time']} — {block['title']}", font_size=dp(18), bold=True, color=get_color_from_hex('#FFD93D'), halign='left', text_size=(dp(310),None), size_hint_y=None, height=dp(34)))
        food_key = block.get('food_key')
        if food_key and food_key in diet_day:
            fc = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(72), padding=[dp(14),dp(10)], spacing=dp(4))
            with fc.canvas.before:
                Color(rgba=get_color_from_hex('#1B4D3E'))
                fc._bg = RoundedRectangle(size=fc.size, pos=fc.pos, radius=[dp(12)])
            fc.bind(size=lambda w,v: setattr(w._bg,'size',v))
            fc.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            fc.add_widget(Label(text=t('today_menu'), font_size=dp(12), bold=True, color=get_color_from_hex('#6BCB77'), halign='left', text_size=(dp(290),None), size_hint_y=None, height=dp(22)))
            fc.add_widget(Label(text=diet_day[food_key], font_size=dp(14), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(290),None), size_hint_y=None, height=dp(30)))
            box.add_widget(fc)
        exercises = block.get('exercises')
        if exercises is None:
            box.add_widget(Label(text=lfk_day['title'], font_size=dp(14), bold=True, color=get_color_from_hex('#D8A8F0'), halign='left', text_size=(dp(310),None), size_hint_y=None, height=dp(28)))
            exercises = [f"• {ex}" for ex in lfk_day['exercises']]
        if exercises:
            box.add_widget(Label(text=t('exercises'), font_size=dp(12), bold=True, color=get_color_from_hex('#A8C5DA'), halign='left', text_size=(dp(310),None), size_hint_y=None, height=dp(24)))
            for ex in exercises:
                ec = BoxLayout(size_hint_y=None, height=dp(42), padding=[dp(14),dp(8)])
                with ec.canvas.before:
                    Color(rgba=get_color_from_hex('#1E3A5F'))
                    ec._bg = RoundedRectangle(size=ec.size, pos=ec.pos, radius=[dp(10)])
                ec.bind(size=lambda w,v: setattr(w._bg,'size',v))
                ec.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
                ec.add_widget(Label(text=ex, font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(290),None), size_hint_y=None, height=dp(26)))
                box.add_widget(ec)
        box.add_widget(Label(text=f'{t("program_day")}: {idx+1} {t("from_30")}', font_size=dp(11), color=get_color_from_hex('#3A4A5A'), halign='center', size_hint_y=None, height=dp(28)))
        content.add_widget(box)
        close_btn = Button(text=t('close'), size_hint_y=None, height=dp(48), background_normal='', background_color=get_color_from_hex('#6BCB77'), color=get_color_from_hex('#FFFFFF'), font_size=dp(15), bold=True)
        wrap = BoxLayout(orientation='vertical')
        wrap.add_widget(content)
        wrap.add_widget(close_btn)
        popup = Popup(title=f"{block['time']} — {block['title']}", content=wrap, size_hint=(0.95,0.82),
                      background_color=get_color_from_hex('#1A2535'), title_color=get_color_from_hex('#FFD93D'), separator_color=get_color_from_hex('#6BCB77'))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class ChatHubScreen(Screen):
    pass


class CommunityScreen(Screen):
    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.chat_box
        msg_row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60), padding=[dp(10),dp(6)], spacing=dp(2))
        with msg_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            msg_row._bg = RoundedRectangle(size=msg_row.size, pos=msg_row.pos, radius=[dp(10),dp(10),dp(2),dp(10)])
        msg_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        msg_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        msg_row.add_widget(Label(text=t('you'), font_size=dp(11), color=get_color_from_hex('#6BCB77'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(18)))
        msg_row.add_widget(Label(text=text, font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(26)))
        box.add_widget(msg_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.chat_scroll, 'scroll_y', 0), 0.1)


class AIChatScreen(Screen):
    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.ai_chat_box
        user_row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60), padding=[dp(10),dp(6)], spacing=dp(2))
        with user_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            user_row._bg = RoundedRectangle(size=user_row.size, pos=user_row.pos, radius=[dp(10),dp(10),dp(2),dp(10)])
        user_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        user_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        user_row.add_widget(Label(text=t('you'), font_size=dp(11), color=get_color_from_hex('#6BCB77'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(18)))
        user_row.add_widget(Label(text=text, font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(26)))
        box.add_widget(user_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.ai_scroll, 'scroll_y', 0), 0.1)
        Clock.schedule_once(lambda dt: self._auto_reply(box), 1.0)

    def _auto_reply(self, box):
        replies_ru = ["Рекомендую проконсультироваться с врачом.","Старайтесь пить 8 стаканов воды в день.","Следите за режимом питания по программе.","Регулярные упражнения ЛФК улучшат самочувствие.","Здоровый сон не менее 8 часов — важно!"]
        replies_en = ["I recommend consulting your doctor.","Try to drink 8 glasses of water daily.","Follow your diet program.","Regular PT exercises will improve your wellbeing.","Healthy sleep of at least 8 hours is important!"]
        replies_kz = ["Дәрігермен кеңесуді ұсынамын.","Күніне 8 стакан су ішуге тырысыңыз.","Бағдарлама бойынша тамақтану режимін сақтаңыз.","Тұрақты ЕДШ жаттығулары өзіңізді жақсы сезінуге көмектеседі.","Кем дегенде 8 сағат ұйықтаңыз!"]
        lang = current_lang[0]
        replies = {'RU': replies_ru, 'EN': replies_en, 'KZ': replies_kz}.get(lang, replies_ru)
        reply = random.choice(replies)
        ai_row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70), padding=[dp(10),dp(6)], spacing=dp(2))
        with ai_row.canvas.before:
            Color(rgba=get_color_from_hex('#1B4D3E'))
            ai_row._bg = RoundedRectangle(size=ai_row.size, pos=ai_row.pos, radius=[dp(2),dp(10),dp(10),dp(10)])
        ai_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        ai_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        ai_row.add_widget(Label(text=t('ai_label'), font_size=dp(11), color=get_color_from_hex('#FFD93D'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(18)))
        ai_row.add_widget(Label(text=reply, font_size=dp(12), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(290),None), size_hint_y=None, height=dp(36)))
        box.add_widget(ai_row)
        Clock.schedule_once(lambda dt: setattr(self.ids.ai_scroll, 'scroll_y', 0), 0.1)


class SupportScreen(Screen):
    def send_message(self, text_input):
        text = text_input.text.strip()
        if not text:
            return
        box = self.ids.support_chat_box
        user_row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60), padding=[dp(10),dp(6)], spacing=dp(2))
        with user_row.canvas.before:
            Color(rgba=get_color_from_hex('#1E3A5F'))
            user_row._bg = RoundedRectangle(size=user_row.size, pos=user_row.pos, radius=[dp(10),dp(10),dp(2),dp(10)])
        user_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        user_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        user_row.add_widget(Label(text=t('you'), font_size=dp(11), color=get_color_from_hex('#6BCB77'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(18)))
        user_row.add_widget(Label(text=text, font_size=dp(13), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(26)))
        box.add_widget(user_row)
        text_input.text = ''
        Clock.schedule_once(lambda dt: setattr(self.ids.support_scroll, 'scroll_y', 0), 0.1)
        Clock.schedule_once(lambda dt: self._auto_reply(box), 1.5)

    def _auto_reply(self, box):
        reply = {"RU":"Спасибо за обращение! Ответим в течение 24 часов.", "EN":"Thank you for reaching out! We'll reply within 24 hours.", "KZ":"Хабарласқаныңызға рахмет! 24 сағат ішінде жауап береміз."}.get(current_lang[0], "Спасибо за обращение!")
        sup_row = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70), padding=[dp(10),dp(6)], spacing=dp(2))
        with sup_row.canvas.before:
            Color(rgba=get_color_from_hex('#3D1F5C'))
            sup_row._bg = RoundedRectangle(size=sup_row.size, pos=sup_row.pos, radius=[dp(2),dp(10),dp(10),dp(10)])
        sup_row.bind(size=lambda w,v: setattr(w._bg,'size',v))
        sup_row.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
        sup_row.add_widget(Label(text=t('support_label'), font_size=dp(11), color=get_color_from_hex('#D8A8F0'), halign='left', text_size=(dp(300),None), size_hint_y=None, height=dp(18)))
        sup_row.add_widget(Label(text=reply, font_size=dp(12), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(290),None), size_hint_y=None, height=dp(36)))
        box.add_widget(sup_row)
        Clock.schedule_once(lambda dt: setattr(self.ids.support_scroll, 'scroll_y', 0), 0.1)


class WeatherScreen(Screen):
    loading    = BooleanProperty(False)
    error_text = StringProperty('')
    selected_city = StringProperty('Алматы')

    WEATHER_CODES = {
        0:'Ясно', 1:'Преим. ясно', 2:'Переменная облачность',
        3:'Пасмурно', 45:'Туман', 48:'Иней',
        51:'Лёгкая морось', 61:'Дождь', 63:'Умеренный дождь',
        65:'Сильный дождь', 71:'Снег', 80:'Ливень', 95:'Гроза',
    }
    _suggestion_popup = None

    def on_enter(self):
        if not self.ids.weather_cards.children:
            self.select_city('Алматы')

    def on_search_text(self, text):
        if self._suggestion_popup:
            try: self._suggestion_popup.dismiss()
            except: pass
            self._suggestion_popup = None
        if len(text) < 1:
            return
        matches = [c for c in KZ_CITIES if text.lower() in c.lower()]
        if not matches:
            return
        content = BoxLayout(orientation='vertical', spacing=dp(2), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        popup_ref = [None]
        for city in matches[:8]:
            btn = Button(text=city, size_hint_y=None, height=dp(44), background_normal='', background_color=get_color_from_hex('#1E3A5F'), color=get_color_from_hex('#FFFFFF'), font_size=dp(14))
            def pick(b, c=city):
                if popup_ref[0]: popup_ref[0].dismiss()
                self.ids.city_search.text = c
                self.select_city(c)
            btn.bind(on_release=pick)
            content.add_widget(btn)
        scroll = ScrollView(size_hint=(1,1))
        scroll.add_widget(content)
        popup_h = min(len(matches[:8]) * dp(46) + dp(20), dp(320))
        popup = Popup(title='', content=scroll, size_hint=(0.88,None), height=popup_h, background_color=get_color_from_hex('#0F1923'), separator_height=0)
        popup_ref[0] = popup
        self._suggestion_popup = popup
        popup.open()

    def select_city(self, city):
        self.selected_city = city
        self.fetch_weather(city)

    def fetch_weather(self, city=None):
        if city is None:
            try: city = self.ids.city_search.text.strip() or 'Алматы'
            except: city = 'Алматы'
        if self._suggestion_popup:
            try: self._suggestion_popup.dismiss()
            except: pass
        self.loading = True
        self.error_text = ''
        self.ids.weather_cards.clear_widgets()
        threading.Thread(target=self._fetch_thread, args=(city.strip(),), daemon=True).start()

    def _fetch_thread(self, city_name):
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_name)}&count=1&language=ru&format=json"
            with urllib.request.urlopen(geo_url, timeout=10) as r:
                geo = json.loads(r.read())
            results = geo.get('results', [])
            if not results:
                Clock.schedule_once(lambda dt: setattr(self, 'error_text', t('city_not_found')))
                Clock.schedule_once(lambda dt: setattr(self, 'loading', False))
                return
            lat = results[0]['latitude']
            lon = results[0]['longitude']
            name = results[0].get('name', city_name)
            wx_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days=3"
            with urllib.request.urlopen(wx_url, timeout=10) as r:
                wx = json.loads(r.read())
            daily = wx['daily']
            day_labels = [t('today'), t('tomorrow'), t('after_tomorrow')]
            data = []
            for i in range(min(3, len(daily['time']))):
                data.append({'day':day_labels[i],'date':daily['time'][i],'desc':self.WEATHER_CODES.get(daily['weathercode'][i],'OK'),'tmax':f"{daily['temperature_2m_max'][i]:.0f}",'tmin':f"{daily['temperature_2m_min'][i]:.0f}",'precip':f"{daily['precipitation_sum'][i]:.1f}",'city':name})
            Clock.schedule_once(lambda dt: self._build_cards(data))
        except Exception as e:
            msg = f'{t("conn_error")}\n{str(e)[:80]}'
            Clock.schedule_once(lambda dt: setattr(self, 'error_text', msg))
            Clock.schedule_once(lambda dt: setattr(self, 'loading', False))

    def _build_cards(self, data):
        self.loading = False
        box = self.ids.weather_cards
        box.clear_widgets()
        colors = ['#1E3A5F','#1B4D3E','#3D1F5C']
        for i, d in enumerate(data):
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140), padding=[dp(16),dp(12)], spacing=dp(6))
            with card.canvas.before:
                Color(rgba=get_color_from_hex(colors[i % 3]))
                card._bg = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(14)])
            card.bind(size=lambda w,v: setattr(w._bg,'size',v))
            card.bind(pos=lambda w,v: setattr(w._bg,'pos',v))
            card.add_widget(Label(text=f"{d['day']}  {d['date']}  •  {d['city']}", font_size=dp(13), bold=True, color=get_color_from_hex('#FFD93D'), halign='left', text_size=(dp(340),None), size_hint_y=None, height=dp(24)))
            card.add_widget(Label(text=d['desc'], font_size=dp(17), bold=True, color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(340),None), size_hint_y=None, height=dp(32)))
            card.add_widget(Label(text=f"{t('max')}: {d['tmax']}°C  •  {t('min')}: {d['tmin']}°C", font_size=dp(14), color=get_color_from_hex('#FFFFFF'), halign='left', text_size=(dp(340),None), size_hint_y=None, height=dp(24)))
            card.add_widget(Label(text=f"{t('precip')}: {d['precip']} {t('mm')}", font_size=dp(12), color=get_color_from_hex('#A8C5DA'), halign='left', text_size=(dp(340),None), size_hint_y=None, height=dp(22)))
            box.add_widget(card)


class SettingsScreen(Screen):
    dark_mode     = BooleanProperty(True)
    notif_screen  = BooleanProperty(True)
    notif_enabled = BooleanProperty(True)
    is_guest      = BooleanProperty(True)
    current_lang_label = StringProperty('RU')

    def on_enter(self):
        self.dark_mode     = get_setting('dark_mode',     True)
        self.notif_screen  = get_setting('notif_screen',  True)
        self.notif_enabled = get_setting('notif_enabled', True)
        self.is_guest      = get_setting('is_guest',      True)
        self.current_lang_label = current_lang[0]

    def toggle_dark(self, value):
        self.dark_mode = value
        set_setting('dark_mode', value)
        apply_theme(value)

    def toggle_notif_screen(self, value):
        self.notif_screen = value
        set_setting('notif_screen', value)

    def toggle_notif(self, value):
        self.notif_enabled = value
        set_setting('notif_enabled', value)

    def open_language_picker(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(16))
        content.add_widget(Label(
            text='Выберите язык / Select language / Тілді таңдаңыз',
            font_size=dp(13), color=get_color_from_hex('#A8C5DA'),
            halign='center', size_hint_y=None, height=dp(40), text_size=(dp(280),None)
        ))
        popup_ref = [None]

        def make_btn(code, label, is_cur):
            btn = Button(
                text=label, size_hint_y=None, height=dp(52),
                background_normal='',
                background_color=get_color_from_hex('#1B4D3E' if is_cur else '#1E2E3E'),
                color=get_color_from_hex('#FFD93D' if is_cur else '#FFFFFF'),
                font_size=dp(15), bold=is_cur
            )
            def on_pick(instance, lc=code):
                current_lang[0] = lc
                set_setting('language', lc)
                if popup_ref[0]:
                    popup_ref[0].dismiss()
                # Перестраиваем все экраны с новым языком
                Clock.schedule_once(lambda dt: App.get_running_app().rebuild_screens(), 0.1)
            btn.bind(on_release=on_pick)
            return btn

        cur = current_lang[0]
        for code, label in [('RU','RU — Русский'), ('EN','EN — English'), ('KZ','KZ — Казакша')]:
            content.add_widget(make_btn(code, label, code == cur))

        cancel_btn = Button(
            text='Закрыть / Close / Жабу',
            size_hint_y=None, height=dp(44),
            background_normal='', background_color=get_color_from_hex('#333333'),
            color=get_color_from_hex('#FFFFFF'), font_size=dp(13)
        )
        content.add_widget(cancel_btn)
        popup = Popup(
            title='Язык / Language / Тіл', content=content,
            size_hint=(0.88,None), height=dp(340),
            background_color=get_color_from_hex('#1A2535'),
            title_color=get_color_from_hex('#FFD93D'),
            separator_color=get_color_from_hex('#6BCB77')
        )
        popup_ref[0] = popup
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def set_pin(self):
        show_popup(t('info'), t('pin_unavailable'))

    def invite_friends(self):
        show_popup(t('invitation'), t('invite_msg'))

    def delete_profile(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(14))
        content.add_widget(Label(text=t('delete_confirm'), halign='center', color=get_color_from_hex('#FFFFFF'), font_size=dp(14)))
        row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        popup = Popup(title=t('delete_title'), content=content, size_hint=(0.85,None), height=dp(180),
                      background_color=get_color_from_hex('#1A2535'), title_color=get_color_from_hex('#FFD93D'))
        yes = Button(text=t('delete'), background_normal='', background_color=get_color_from_hex('#E74C3C'))
        no  = Button(text=t('cancel'), background_normal='', background_color=get_color_from_hex('#555555'))
        def confirm(*a):
            try: store.delete('settings')
            except: pass
            popup.dismiss()
            self.manager.current = 'main'
        yes.bind(on_release=confirm)
        no.bind(on_release=popup.dismiss)
        row.add_widget(no)
        row.add_widget(yes)
        content.add_widget(row)
        popup.open()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'app_screen'


# ──────────────────────────────────────────────────
#  APP — rebuild_screens для смены языка
# ──────────────────────────────────────────────────
class HealthMateApp(App):
    # Этот property используется в kv как триггер для обновления текстов
    # Когда он меняется — Kivy пересчитывает все выражения которые его читают
    lang = StringProperty('RU')

    def build(self):
        self.title = 'HealthMate 2.3'
        saved_lang = get_setting('language', 'RU')
        if saved_lang in TRANSLATIONS:
            current_lang[0] = saved_lang
        self.lang = current_lang[0]
        dark = get_setting('dark_mode', True)
        apply_theme(dark)
        return self._build_sm()

    def _build_sm(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(AppScreen(name='app_screen'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(ReminderScreen(name='reminder'))
        sm.add_widget(ChatHubScreen(name='chat_hub'))
        sm.add_widget(CommunityScreen(name='community'))
        sm.add_widget(AIChatScreen(name='ai_chat'))
        sm.add_widget(SupportScreen(name='support'))
        sm.add_widget(WeatherScreen(name='weather'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

    def rebuild_screens(self):
        """Меняет app.lang — Kivy пересчитывает все t() в kv автоматически"""
        # app.lang используется в kv выражениях — изменение триггерит перерисовку
        self.lang = current_lang[0]
        # Также обновляем SettingsScreen
        try:
            s = self.root.get_screen('settings')
            s.current_lang_label = current_lang[0]
        except Exception:
            pass

    def _refresh_labels(self, widget):
        pass

if __name__ == '__main__':
    HealthMateApp().run()
