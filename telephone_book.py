import os
import json
import sqlite3
from easygui import *


DATA_JSON = "tel.json"
DATA_SQL = "telSQLLITE.bd"



def save_sql(data) : 
    connection = sqlite3.connect(DATA_SQL)
    cursor = connection.cursor()
    table=['Users','email','phone']
    sqid=0
    sqid2=0
    sqid3=0
    
    for i in table:
        cursor.execute(f'DROP TABLE IF EXISTS {i};')
        # print(cursor.fetchall())
        connection.commit()
    
    cursor.execute('''CREATE TABLE Users (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age TEXT NOT NULL
    )
    ''')
    connection.commit()
    
    cursor.execute('''CREATE TABLE email (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mail TEXT NOT NULL,
    UserID INT NOT NULL,
    FOREIGN KEY (UserID)  REFERENCES Users (id)
    )
    ''')
    connection.commit()
    
    cursor.execute('''CREATE TABLE phone (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone TEXT NOT NULL,
    UserID INT NOT NULL,
    FOREIGN KEY (UserID)  REFERENCES Users (id)
    )
    ''')
    connection.commit()
    
    print("SAVE\n[▬▬\t]")
    
    for key in list(data.keys()):# заполнение БД
        
        cursor.execute(f'INSERT INTO Users (id, name, age) VALUES ("{str(sqid)}","{key}", "{data[key]["birthday"][0]}");')
        connection.commit()
        
        for a in data[key]['phones']:
            cursor.execute(f'INSERT INTO phone (id, phone, UserID) VALUES ("{str(sqid2)}","{str(a)}", "{str(sqid)}");')
            connection.commit()
            sqid2 +=1
        
        for a in data[key]['email']:
            cursor.execute(f'INSERT INTO email (id, mail, UserID) VALUES ("{str(sqid3)}","{str(a)}", "{str(sqid)}");')
            connection.commit()   
            sqid3 +=1
        
        sqid += 1
        
    print("SAVE\n[▬▬▬▬▬▬] 100%")    
    print("↑sql[√]↑") 
    connection.close()
    
def load_sql() :
    connection = sqlite3.connect(DATA_SQL)
    cursor = connection.cursor()
    data={}
    
    cursor.execute('SELECT name,id,age FROM Users')
    users = cursor.fetchall()
    
    for line in users:
        print(line[0])
        
        
        cursor.execute(f'SELECT mail FROM email WHERE UserID = "{line[1]}"')
        mail = cursor.fetchall()
        
        cursor.execute(f'SELECT phone FROM phone WHERE UserID = "{line[1]}"')
        phone = cursor.fetchall()
        
        print(mail)
        print(phone)
        
        print()

        
        data[str(line[0])]={ 'phones': [phone[0][0]],'birthday': [line[2]],'email': [mail[0][0]] }
        
        if len(phone) > 1:
            data[str(line[0])]['phones'].append(phone[1][0])
        if len(mail) > 1:
            data[str(line[0])]['email'].append(mail[1][0])
        
        
    connection.close()
    return(data)

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
        data = load_sql() # load_sql заглушка
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
    print("SAVE\n[▬\t]")
    save_sql(data)
        
    
    
    
print('Запуск телефоной книги')
main_menu()
