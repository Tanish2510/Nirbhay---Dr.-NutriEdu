import logging
from Backend.meal_db import get_meal_data

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class MealSuggestions:
    def __init__(self):
        pass

    def get_meal_suggestion(self, dietary_preference, calories, category, allergies):
        """
        Fetches meal suggestions based on dietary preference, calorie intake, and category.
        :param dietary_preference: 'Vegetarian', 'Non-Vegetarian', 'Vegan', etc.
        :param calories: Target calories for the meal.
        :param category: Meal category ('Breakfast', 'Lunch', 'Dinner', 'Snack').
        :param allergies: Comma-separated string of allergies (or None).
        :return: List of meal options or a message if no meals are found.
        """
        logger.info(f"🚀 Entering get_meal_suggestion() with dietary_preference={dietary_preference}, "
                    f"calories={calories}, category={category}, allergies={allergies}")

        # 🛑 Ensure category is valid
        if not category:
            logger.error("❌ ERROR: Category is missing or None!")
            return {"message": "Meal category is required."}

        # Standardizing category names (handles singular/plural variations)
        category_mapping = {
            "breakfast": "Breakfast",
            "lunch": "Lunch",
            "dinner": "Dinner",
            "snacks": "Snack",  # Mapping 'Snacks' -> 'Snack'
            "snack": "Snack"  # Handling singular/plural
        }
        category = category.strip().lower()
        category = category_mapping.get(category, category)  # Default to same category if no match

        # 🛑 Fetch meals from the database (✅ FIX: Added category as an argument)
        try:
            meals = get_meal_data(dietary_preference, category)  # ✅ FIXED: Passing category argument
            logger.info(f"📌 Retrieved {len(meals) if meals else 0} meals from database for {dietary_preference}, category={category}")
        except Exception as e:
            logger.error(f"❌ ERROR: Failed to fetch meals! Exception: {e}")
            return {"message": f"Error fetching meal data: {str(e)}. Please try again later."}

        if not meals:
            logger.warning("⚠️ No meals found for this dietary preference and category.")
            return {"message": "No meals found for the selected dietary preference and category."}

        # ✅ Debugging: Print first 5 meals to check if data is retrieved correctly
        logger.debug(f"📌 Sample meals: {meals[:5]}...")

        # 🛑 Ensure allergies is properly formatted (handles None case)
        allergy_list = [allergy.strip().lower() for allergy in (allergies or "").split(",") if allergy.strip()]

        # Filtering meals based on calorie intake and category
        recommended_meals = []
        for meal in meals:
            # 🛑 Skip meal if required fields are missing
            if not isinstance(meal, dict):
                logger.warning("⚠️ Skipping invalid meal entry (not a dictionary)!")
                continue
            if 'calories' not in meal or 'category' not in meal or 'meal_name' not in meal:
                logger.warning(f"⚠️ Skipping meal due to missing data: {meal}")
                continue

            meal_name = meal.get("meal_name", "Unknown")  # Default name for missing values
            logger.debug(f"🔍 Checking meal: {meal_name} ({meal['category']}) with {meal['calories']} kcal")

            # Filtering based on calories and category
            if meal['calories'] <= calories and meal['category'].strip().lower() == category.lower():
                logger.info(f"✅ Meal '{meal_name}' matches the criteria!")
                recommended_meals.append(meal)
            else:
                logger.debug(f"⚠️ Meal '{meal_name}' does not match the calorie or category criteria.")

        # 🛑 Final check if meals were found
        if not recommended_meals:
            logger.warning(f"⚠️ No meals match the calorie criteria for {category}.")
            return {"message": f"No {category} meals found matching the given calorie criteria."}

        logger.info(f"✅ Found {len(recommended_meals)} recommended meals for {category}.")
        return recommended_meals