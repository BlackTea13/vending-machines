class Config:
    MYSQL_HOST = "127.0.0.1:13306"
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "vending-pw"
    MYSQL_DATABASE = "vending_machines"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
