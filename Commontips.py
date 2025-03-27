# nutritional_health_backend.py
import json

class NutritionalHealthBackend:
    def __init__(self):
        # Dictionary of health conditions and their recommendations
        self.health_recommendations = {
            "diabetes": [
                "Limit carbohydrate intake and monitor blood sugar levels",
                "Include high-fiber foods like vegetables, legumes, and whole grains",
                "Stay hydrated with water or unsweetened beverages",
                "Include cinnamon in your diet, which may help with blood sugar regulation",
                "Exercise regularly with activities like walking for 30 minutes daily"
            ],
            "hypertension": [
                "Reduce sodium intake to less than 2,300mg per day",
                "Follow the DASH diet (Dietary Approaches to Stop Hypertension)",
                "Practice stress reduction techniques like deep breathing or meditation",
                "Consume potassium-rich foods like bananas, potatoes, and leafy greens",
                "Limit alcohol consumption and avoid smoking"
            ],
            "obesity": [
                "Focus on portion control and mindful eating practices",
                "Increase physical activity gradually, aiming for 150 minutes per week",
                "Choose whole foods over processed foods when possible",
                "Drink water before meals to help reduce food intake",
                "Get adequate sleep, aiming for 7-9 hours per night"
            ],
            "arthritis": [
                "Include anti-inflammatory foods like fatty fish, nuts, and olive oil",
                "Apply hot and cold therapy to affected joints",
                "Practice gentle exercises like swimming or water aerobics",
                "Maintain a healthy weight to reduce pressure on joints",
                "Try turmeric as a natural anti-inflammatory supplement"
            ],
            "indigestion": [
                "Eat smaller, more frequent meals throughout the day",
                "Avoid lying down immediately after eating",
                "Try ginger tea or peppermint tea for natural relief",
                "Reduce intake of spicy foods, caffeine, and alcohol",
                "Practice stress reduction techniques as stress can worsen symptoms"
            ],
            "constipation": [
                "Increase dietary fiber intake with fruits, vegetables, and whole grains",
                "Stay well-hydrated throughout the day",
                "Establish a regular bathroom routine",
                "Try adding ground flaxseeds to your meals",
                "Engage in regular physical activity to promote bowel movement"
            ],
            "acid reflux": [
                "Avoid trigger foods like citrus, tomatoes, chocolate, and caffeine",
                "Don't eat within 3 hours of bedtime",
                "Sleep with your head elevated",
                "Try apple cider vinegar diluted in water before meals",
                "Chew food thoroughly and eat slowly"
            ],
            "headache": [
                "Stay hydrated and avoid dehydration triggers",
                "Apply a cold or warm compress to your head or neck",
                "Practice relaxation techniques like deep breathing or meditation",
                "Maintain a regular sleep schedule",
                "Try peppermint or lavender essential oil for tension headaches"
            ],
            "insomnia": [
                "Maintain a consistent sleep schedule, even on weekends",
                "Avoid caffeine and screen time before bed",
                "Create a relaxing bedtime routine",
                "Try chamomile tea or valerian root tea before sleep",
                "Keep your bedroom cool, dark, and quiet"
            ],
            "allergies": [
                "Use a HEPA air purifier in your home",
                "Rinse sinuses with saline solution",
                "Try local honey to build tolerance to local pollen",
                "Use dust-mite proof covers on bedding",
                "Track pollen counts and limit outdoor activities on high pollen days"
            ]
        }

    def process_health_info(self, health_description):
        """Process the health description and return identified conditions and recommendations."""
        description = health_description.lower()
        identified_conditions = []

        for condition in self.health_recommendations.keys():
            if condition in description:
                identified_conditions.append(condition)

        if not identified_conditions:
            conditions_text = "We couldn't identify specific conditions from your description, but here are some general nutritional tips:"
            general_tips = [
                "Stay hydrated by drinking at least 8 glasses of water daily",
                "Eat a variety of colorful fruits and vegetables",
                "Limit processed foods and added sugars",
                "Include protein sources in each meal",
                "Consider mindful eating practices to improve digestion"
            ]
            recommendations = "\n".join(f"• {tip}" for tip in general_tips)
        else:
            conditions_text = "Based on your input, we've identified these potential concerns: " + ", ".join(identified_conditions)
            all_recommendations = []
            for condition in identified_conditions:
                all_recommendations.append(f"\n--- {condition.upper()} ---")
                for rec in self.health_recommendations[condition]:
                    all_recommendations.append(f"• {rec}")
            recommendations = "\n".join(all_recommendations)

        return conditions_text, recommendations

    def book_appointment(self, name, phone, email, specialist, date, time):
        """Generate a confirmation message and save appointment data to a JSON file."""
        appointment_data = {
            "name": name,
            "phone": phone,
            "email": email,
            "specialist": specialist,
            "date": date,
            "time": time
        }

        # Save appointment data to a JSON file
        self.save_appointment_data(appointment_data)

        confirmation_message = f"""
        Dear {name},

        Your appointment has been confirmed with the following details:

        Specialist: {specialist}
        Date: {date}
        Time: {time}

        Please arrive 15 minutes before your scheduled time.

        For cancellations or rescheduling, please call our office at 555-123-4567.
        """
        return confirmation_message

    def save_appointment_data(self, appointment_data):
        """Save appointment data to a JSON file."""
        try:
            with open("appointments.json", "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.append(appointment_data)

        with open("appointments.json", "w") as f:
            json.dump(existing_data, f, indent=4)

    def load_appointment_data(self):
        """Load appointment data from the JSON file."""
        try:
            with open("appointments.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []