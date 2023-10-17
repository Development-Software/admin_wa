import mysql.connector
import os

config_db = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
}
whatsapp = {
    "Token_WA": os.getenv("TOKEN_WA"),
}


def connect_db():
    db = mysql.connector.connect(**config_db)
    return db


def token_wa():
    return whatsapp["Token_WA"]
