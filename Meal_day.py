import logging
from Interface.modules.meal_suggestion import MealSuggestions
from Interface.modules.calorie_calculator import calculate_daily_calories

# ✅ Configure logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MealDay:
    def __init__(self, user_data):
        """
        Initializes the MealDay class with user data.
        Ensures user data is provided and initializes meal suggestion module.
        """
        logger.info("🔹 Initializing MealDay with user data...")

        # 🔍 Ensure valid user data is provided
        if not user_data:
            logger.error("❌ ERROR: No user data provided!")
            raise ValueError("User data is required to generate a meal plan.")

        self.user_data = user_data
        self.meal_suggestions = MealSuggestions()

        logger.info("✅ MealDay: Initialization complete.")

    def meal_plan_for_day(self):
        """
        Generates a meal plan for the day based on user input.
        Calls the calorie calculator and retrieves meal suggestions.
        """
        logger.info("🔹 Generating meal plan...")
        logger.info(f"📌 Debug: User data received in MealDay: {self.user_data}")

        # 🔹 Validate required user data fields
        required_fields = ["age", "gender", "activity_level", "bmi_category", "health_goal"]
        missing_fields = [field for field in required_fields if field not in self.user_data]

        if missing_fields:
            logger.error(f"❌ ERROR: Missing user data fields: {missing_fields}")
            return {"message": f"Missing required fields: {', '.join(missing_fields)}."}

        # ✅ Step 1: Calculate daily calories
        try:
            daily_calories = calculate_daily_calories(
                age=self.user_data["age"],
                gender=self.user_data["gender"],
                activity_level=self.user_data["activity_level"],
                bmi_category=self.user_data["bmi_category"]  # ✅ CORRECT
            ) 
            logger.info(f"✅ Calculated daily calories: {daily_calories}")
        except Exception as e:
            logger.error(f"❌ ERROR calculating daily calories: {e}")
            return {"message": f"Error calculating daily calories: {str(e)}."}

        # ✅ Step 2: Define calorie distribution for meals
        meal_distribution = {
            "Breakfast": 0.15 * daily_calories,
            "Lunch": 0.45 * daily_calories,
            "Dinner": 0.30 * daily_calories,
            "Snacks": 0.1 * daily_calories
        }
        logger.info(f"📌 Meal distribution: {meal_distribution}")

        # ✅ Step 3: Fetch meal suggestions for each category
        meal_plan = {}
        for meal, calories in meal_distribution.items():
            logger.info(f"🔍 Fetching {meal} suggestions for {calories:.2f} kcal...")

            try:
                # 🔹 Fetch meal suggestions based on user preferences
                meal_suggestion = self.meal_suggestions.get_meal_suggestion(
                    dietary_preference=self.user_data.get("dietary_preference"),
                    calories=calories,
                    category=meal,  # ✅ Pass meal category
                    allergies=self.user_data.get("allergies")
                )
                logger.info(f"📌 Debug: Received {meal} suggestion: {meal_suggestion}")

                # ✅ Handle case where no meals are found
                if not meal_suggestion:
                    logger.warning(f"⚠️ No meals found for {meal}. Adding a default message.")
                    meal_suggestion = ["No suitable meals found"]

                meal_plan[meal] = meal_suggestion
                logger.info(f"✅ {meal}: {meal_plan[meal]}")

            except KeyError as ke:
                logger.error(f"❌ KeyError while fetching {meal}: {ke}")
                meal_plan[meal] = ["Error fetching meal suggestion (KeyError)"]

            except Exception as e:
                logger.error(f"❌ ERROR while fetching {meal}: {str(e)}")
                meal_plan[meal] = ["Error fetching meal suggestion"]

        # ✅ Final step: Validate meal plan structure
        for meal, suggestions in meal_plan.items():
            if not isinstance(suggestions, list):
                logger.error(f"❌ Invalid data structure for {meal}: {suggestions}")
                meal_plan[meal] = ["Invalid meal suggestion data"]

        # ✅ Final step: Return the meal plan
        logger.info(f"✅ Final meal plan: {meal_plan}")
        
        # Return the formatted meal plan to the UI code
        return self.format_meal_plan(meal_plan)

    def format_meal_plan(self, meal_plan):
        """Formats the meal plan dictionary into a readable string."""
        if not meal_plan:
            return "No meal plan available."

        formatted_text = ""
        for category, meals in meal_plan.items():
            formatted_text += f"\n➡ <b>{category}</b>:\n"
        
            # Check if meals is a string
            if isinstance(meals, str):
                formatted_text += f"   • {meals}\n"  # Display the string directly
            # Check if meals is a dictionary
            elif isinstance(meals, dict):
                if "message" in meals:
                    formatted_text += f"   • {meals['message']}\n"
                else:
                    formatted_text += "   • No meals available.\n"
            # Check if meals is a list
            elif isinstance(meals, list) and meals:
                for meal in meals:
                    formatted_text += f"   • {meal.get('meal_name', 'Unknown')} ({meal.get('calories', 0)} kcal)\n"
            else:
                formatted_text += "   • No meals available.\n"

        return formatted_text