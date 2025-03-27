import logging
from Backend.db_config import get_db_connection

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

def get_meal_data(dietary_preference, category):
    logger.info(f"🛠 Fetching meal data for dietary preference: {dietary_preference} and category: {category}")

    # ✅ Debug: Test database connection
    conn = get_db_connection()
    if not conn:
        logger.error("❌ ERROR: Database connection failed! Check db_config.py")
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        # ✅ Debug: Log the preference before using it
        logger.debug(f"🔍 Raw dietary preference input: {dietary_preference}")

        if dietary_preference.lower() == "vegetarian":
            dietary_preference = "Yes"  # Assuming 'veg' column stores 'Yes'/'No'
        elif dietary_preference.lower() == "non-vegetarian":
            dietary_preference = "No"

        # ✅ Debug: SQL Query Execution
        query = """
        SELECT meal_name, calories, protein, carbs, fat, fiber, category
        FROM meal_info 
        WHERE veg = %s AND category = %s
        """
        logger.debug(f"🔍 Executing query: {query} with parameters ({dietary_preference}, {category})")

        cursor.execute(query, (dietary_preference, category))
        meals = cursor.fetchall()

        if not meals:
            logger.warning("⚠️ No meals found in the database for the given preference and category!")
        else:
            logger.info(f"✅ Meals fetched: {len(meals)}")
            logger.debug(f"📌 Sample meal data: {meals[:5]}")  # Print first 5 meals for debugging

    except Exception as e:
        logger.error(f"❌ ERROR: Failed to fetch meal data! Exception: {e}")
        meals = []
    finally:
        conn.close()
        logger.info("🔌 Database connection closed.")

    return meals

# ✅ Test connection separately
if __name__ == "__main__":
    logger.info("🔄 Testing database connection and meal retrieval...\n")
    test_data = get_meal_data("Vegetarian", "Breakfast")
    logger.info(f"🔍 Test meal data output: {test_data}")