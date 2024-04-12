import json
import sqlite3
from easygui import *
import os

DATA_JSON = "tel.json"
DATA_SQL = "telSQLLITE.bd"

def save_js(phonebook) :
    with open(DATA_JSON, "w", encoding='utf-8') as write_file:
        json.dump(phonebook, write_file, ensure_ascii=False)

def load_js() :
    with open(DATA_JSON, "r", encoding='utf-8') as read_file:
        ph = json.load(read_file) 
    return ph 

def print_key(data):
    atr = list(data.keys())
    print(*atr)
    return choicebox("Выберите абонента", "Главная форма", atr)

def search(key):
    pass
    
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
'''{
    "дядя Ваня": { 'phones': [123], 
                  'birthday': ['01.01.1960'], 
                  'email': ["vanya@mail.ru"] } ,
    "дядя Вася": { 'phones': [22222], 
                  'birthday': ['01.01.2000'], 
                  'email': ["vanya@mail.ru"] } 
}'''



# if not os.path.exists(DATA_JSON):
    # save_js(phonebook)
# data = load_js()
# 
# print(data['дядя Ваня'] ['phones'][0])  
# print( print_key(data) )



def main_menu():
    menu=['Открыть справочник', 'Импортировать', 'Экспартировать', 'Выход']
    data=0
    if os.path.exists(DATA_SQL):
        # load_sql
        print("sql")
    else:
        msgbox("""Ошибка подключения к Базе Данных
        Импорт будет произведен из файла tel.json""","Ошибка БД", ok_button="Пуск")
        if not os.path.exists(DATA_JSON):
            msgbox("""Ошибка загрузки файла tel.json 
            Бует создан шаблоный tel.json""", "Ошибка Импорта", ok_button="Пуск")
            save_js(phonebook)
        data = load_js()
    print(data)
    
    

main_menu()