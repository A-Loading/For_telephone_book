import os
import json
import sqlite3
from easygui import *


DATA_JSON = "tel.json"
DATA_SQL = "telSQLLITE.bd"



def save_sql(data) : 
    print('sql заглушка')

def load_sql(data) : # load_sql заглушка
    pass

def save_js(phonebook) :
    with open(DATA_JSON, "w", encoding='utf-8') as write_file:
        json.dump(phonebook, write_file, ensure_ascii=False)

def load_js() :
    with open(DATA_JSON, "r", encoding='utf-8') as read_file:
        ph = json.load(read_file) 
    return ph 

def print_key(data):
    atr = list(data.keys())
    # print(*atr)
    return choicebox("Выберите абонента", "Главная форма", atr)

def search(data):
    pass
    
def import_():
    if not os.path.exists(DATA_JSON):
        print('ERR ↓•JSON•↓')
        msgbox("""Ошибка загрузки файла tel.json 
Бует создан шаблоный tel.json""", "Ошибка Импорта", ok_button="Пуск")
                
        phonebook = {
                    "милиция": { 'phones': ['02'], 
                                 'birthday': ['-'], 
                                 'email': ['-'] } ,
                    "скорая помощь": { 'phones': ['03'], 
                                  'birthday': ['-'], 
                                  'email': ['-'] } ,
                    "пожарная охрана": { 'phones': ['01'], 
                                  'birthday': ['-'], 
                                  'email': ['-'] }
                 }
        save_js(phonebook)
        print('[√] ↑•JSON•↑')
    return load_js()


def main_menu():
    menu=['Открыть справочник', 'Импортировать', 'Экспортировать', 'Выход']
    data=0
    if os.path.exists(DATA_SQL):
        load_sql() # load_sql заглушка
    else:
        print('ERR ↓•SQL•↓')
        msgbox("""Ошибка подключения к Базе Данных
Загрузка будет произведена из файла tel.json""","Ошибка БД", ok_button="Пуск")
        data = import_()
        print('[√] load •data•')
    print('♥♦♣♠',data)
    choice = 0
    while (choice != "Выход") and (choice != None):
        choice = choicebox("Меню", "Телефоная книга | Главное меню", menu)
        print(choice)
        if choice == 'Открыть справочник':
            data = search(data)
        elif choice == 'Импортировать':
            data = import_()
            print('[√] load •data•')
        elif choice == 'Экспортировать':
            save_js(data)
            print('[√] ↑•JSON•↑')
    save_sql(data)
        
    
    
    
print('Запуск телефоной книги')
main_menu()


