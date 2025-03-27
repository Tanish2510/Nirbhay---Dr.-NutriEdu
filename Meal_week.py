import mysql.connector

class MealWeekHandler:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="HealthKiosk"
        )
        self.cursor = self.conn.cursor()

    def fetch_meal_plan_week(self, dietary_preference):
        """Fetch personalized meal plan for a week based on dietary preference"""
        query = """SELECT meal_plan FROM meals_week WHERE dietary_preference=%s LIMIT 1"""
        self.cursor.execute(query, (dietary_preference,))
        result = self.cursor.fetchone()
        return result[0] if result else "No meal plan found."

    def close(self):
        self.conn.close()
