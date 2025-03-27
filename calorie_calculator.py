def calculate_daily_calories(age, gender, activity_level, bmi_category="Normal"):
    """
    Calculates daily calorie requirement based on user profile.
    """
    # Add this at the start of calculate_daily_calories():
    valid_categories = ["Underweight", "Normal", "Overweight"]
    if bmi_category not in valid_categories:
        raise ValueError(f"Invalid BMI category: {bmi_category}")
    
    # Validate gender input
    if gender not in ["Male", "Female"]:
        raise ValueError("Invalid gender. Must be 'Male' or 'Female'.")

    # Set base calories based on gender and age
    base_calories = 2500 if gender == "Male" else 2000  # Default for young adults
    if age >= 30:
        base_calories -= 100
    if age >= 50:
        base_calories -= 200

    # Adjust for BMI category
    bmi_adjustments = {"Underweight": 300, "Overweight": -300, "Normal": 0}
    base_calories += bmi_adjustments.get(bmi_category, 0)

    # Adjust for activity level
    activity_multiplier = {"Sedentary": 1.2, "Moderate": 1.5, "Active": 1.8}
    if activity_level not in activity_multiplier:
        raise ValueError("Invalid activity level. Choose from 'Sedentary', 'Moderate', 'Active'.")

    final_calories = round(base_calories * activity_multiplier[activity_level])

    return final_calories