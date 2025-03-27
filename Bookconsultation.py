class NutritionKioskLogic:
    def __init__(self):
        self.selected_doctor = None
        self.data = {}  # Store all patient data by phone number

    def select_doctor(self, doctor_id, doctor_name):
        """
        Select a doctor based on the given doctor id and name.
        """
        self.selected_doctor = {"id": doctor_id, "name": doctor_name}
        return self.selected_doctor

    def save_patient_data(self, name, phone, age, gender, is_child, nutrition_concern, selected_doctor):
        """
        Save patient data to the internal dictionary and return it.
        """
        # Create the patient data dictionary
        patient_data = {
            "name": name,
            "phone": phone,
            "age": age,
            "gender": gender,
            "is_child": is_child,
            "nutrition_concern": nutrition_concern,
            "doctor": selected_doctor  # Save the selected doctor information
        }

        # Store the patient data in the dictionary with phone number as the key
        self.data[phone] = patient_data

        # Return the patient data to be used in confirmation generation
        return patient_data

    def validate_patient_info(self, name, phone, age):
        """
        Validates patient information (e.g., name, phone, and age).
        Returns False if any validation fails.
        """
        if not name:
            return False, "Name cannot be empty."
        
        if not phone or len(phone) != 10 or not phone.isdigit():
            return False, "Phone number must be a 10-digit number."
        
        if not (1 <= age <= 120):
            return False, "Age must be between 1 and 120."
        
        return True, "Valid"

    def generate_confirmation_text(self, patient_data):
        """
        Generates a confirmation message based on the patient data.
        """
        # Ensure all required fields are available in the patient data
        if 'name' not in patient_data or 'phone' not in patient_data:
            raise KeyError("'name' or 'phone' key is missing in the patient data")

        confirmation_text = (
            f"Patient: {patient_data['name']}\n"
            f"Phone: {patient_data['phone']}\n"
            f"Age: {patient_data['age']}\n"
            f"Gender: {patient_data['gender']}\n"
            f"Is Child: {'Yes' if patient_data['is_child'] else 'No'}\n"
            f"Nutrition Concern: {patient_data['nutrition_concern']}\n"
            f"Selected Doctor: {patient_data['doctor']['name']} (ID: {patient_data['doctor']['id']})"
        )
        return confirmation_text
