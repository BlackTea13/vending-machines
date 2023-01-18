import os
import yaml

class Config:
    MYSQL_HOST = '172.22.176.1:3306'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '0427'
    MYSQL_DATABASE = 'vending_machines'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    