import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Keerdbms@26',  # 🔒 change to your MySQL password
        db='job_tracker',
        cursorclass=pymysql.cursors.DictCursor
    )
