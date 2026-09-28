#Импортируем библиотеку
import os

class Config():
    #Подключаем базу данных sql
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:2134567819@localhost:5432/peresdaha_db"
    #Отключаем трекинг модификаций
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_ECHO = False