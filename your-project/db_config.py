import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mealplanner",
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        return None
