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
    return choicebox("Выберите абонента", "Телефонная книга | выбор контакта", atr)

def add_tel(data):
    fieldNames = ["фио", "тел","доп тел", "почта","доп почта", "дата" ]
    fieldValues = multpasswordbox("введите даные", "Новый контакт", fieldNames)
    if fieldValues == None or fieldValues[0] == '' :
        print('[X→]')
        return data

    if not fieldValues[0] in data:
        for i in fieldValues:
            if i == '':
                i='-'
        data[fieldValues[0]]={ 'phones': [fieldValues[1]],'birthday': [fieldValues[5]],'email': [fieldValues[3]] }
        
        if fieldValues[2] != '-':
            data[fieldValues[0]]['phones'].append(fieldValues[2])
        if fieldValues[4] != '-':
            data[fieldValues[0]]['email'].append(fieldValues[4])
    else:
        msgbox("""Ошибка
такое имя уже есть""","Ошибка БД", ok_button="Далее")
    
    print(data.keys())
    
    return data

def del_tel(data,key):
    if key == None:
        return data
    data1 = {}
    for i in data:
        if i != key:
            data1[i]=data[i]
    return data1

def print_data(key,data):
    text = "фио : "+str(key)+"\t дата рождения : "+str(data[key]['birthday'][0])+"\n номера: "
    for i in data[key]['phones']:
        text = str(text)+" "+str(i)+"|"
    text = str(text)+"\n email's : "
    for i in data[key]['email']:
        text = str(text)+" "+str(i)+"|"
    return(text)

def upd_feld(data,key,choice,feld,num=0):
    output = enterbox("Поле \t"+str(choice), "изменение", data[key][feld][num])
    print("[→↓]"+str(output))
    data[key][feld][num] = output
    return(data)

def upd_key(data,key):
    output = enterbox("Поле \t фио", "изменение", key)
    if output == None or output == key or output == '':
        print("[X→]")
        return(data,key)
    if not output in data:
        data[output]=data[key]
    else:
        msgbox("""Ошибка
такое имя уже есть""","Ошибка БД", ok_button="Далее")
        print("[X→]")
        return(data,key)
    
    
    return (data , output)
    
def upd_tel(data):
    key = print_key(data)
    menu=["фио", "тел","доп тел", "почта","доп почта", "дата рождения"]
    choice='s'
    while choice != None:
        text = print_data(key,data)
        print(text)
        choice = choicebox(text, "Телефоная книга | Редактирование", menu)
        if choice == "фио":
            data,key2 = upd_key(data,key)
            data1 = del_tel(data,key)
            if data1 != data:
                print('[→√]')
                data = data1
            key=key2
        elif choice == "тел":
            data = upd_feld(data,key,choice,'phones')
        elif choice == "доп тел":
            if len(data[key]['phones']) == 1:
                data[key]['phones'].append("-")
            data = upd_feld(data,key,choice,'phones',1)
        elif choice == "почта":
            data = upd_feld(data,key,choice,'email')
        elif choice == "доп почта":
            if len(data[key]['email']) == 1:
                data[key]['email'].append("-")
            data = upd_feld(data,key,choice,'email',1)
        elif choice == "дата рождения":
            data = upd_feld(data,key,choice,'birthday')        
        print(str(choice)+"\t--------\t---------\t [√→?]")
              
    return(data)
    
def search(data):
    
    menu=['просмотр', 'изменить', 'добавить', 'удалить']
    choice = choicebox("Меню", "Телефоная книга | Главное меню", menu)
    print(choice)
    if choice == 'добавить':
        data1 = add_tel(data)
        if data1 != data:
            print('[→√]')
            data = data1
    elif choice == 'просмотр':
        key = print_key(data)
        if key == None:
            return data
        text = print_data(key,data)
        print(*text)
        msgbox( text , key, ok_button="дальше")
    elif choice == 'удалить':
        key = print_key(data)
        data1 = del_tel(data,key)
        if data1 != data:
            print('[→√]')
            data = data1
    elif choice == 'изменить':
        data = upd_tel(data)
    
    
    return data
    
    

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


