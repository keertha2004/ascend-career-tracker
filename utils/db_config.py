import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="dpg-d1n924umcj7s73brdnrg-a.singapore-postgres.render.com",
        database="ascend_tracker_db",
        user="ascend_tracker_db_user",
        password="yH8bOkDeBoV1EwOscQ1epHr9fdhEHr2c",
        port=5432
    )
