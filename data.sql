Create database mealplanner;
USE  mealplanner;

CREATE TABLE users (
    u_id INT PRIMARY KEY UNIQUE,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    bmi FLOAT NOT NULL,
    bmi_category VARCHAR(50) NOT NULL,
    dietary_preference VARCHAR(50) CHECK (dietary_preference IN ('Vegetarian', 'Non-Vegetarian')),
    gender VARCHAR(1),
    activity_level VARCHAR(50),
    allergies TEXT NOT NULL
);

INSERT INTO users (u_id, name, age, bmi, bmi_category, dietary_preference, gender, activity_level, allergies) VALUES
(1, 'Aarav Sharma', 29, 22.5, 'Normal', 'Vegetarian', 'M', 'Moderate', 'Peanuts'),
(2, 'Neha Verma', 35, 27.3, 'Overweight', 'Non-Vegetarian', 'F', 'High', 'None'),
(3, 'Rohan Iyer', 42, 18.9, 'Underweight', 'Vegetarian', 'M', 'Low', 'Gluten'),
(4, 'Priya Nair', 31, 24.6, 'Normal', 'Non-Vegetarian', 'F', 'Moderate', 'Shellfish'),
(5, 'Vikram Das', 26, 30.2, 'Obese', 'Vegetarian', 'M', 'High', 'Dairy'),
(6, 'Ananya Kapoor', 38, 26.1, 'Overweight', 'Vegetarian', 'F', 'Low', 'Soy'),
(7, 'Suresh Menon', 50, 21.8, 'Normal', 'Non-Vegetarian', 'M', 'Moderate', 'None'),
(8, 'Meera Joshi', 22, 19.7, 'Normal', 'Vegetarian', 'F', 'High', 'Nuts'),
(9, 'Rahul Singh', 45, 32.5, 'Obese', 'Non-Vegetarian', 'M', 'Low', 'Eggs'),
(10, 'Kavita Rao', 28, 23.4, 'Normal', 'Vegetarian', 'F', 'Moderate', 'Seafood');

CREATE TABLE meal_info (
    m_id INT PRIMARY KEY,
    meal_name VARCHAR(20) UNIQUE NOT NULL,
    category ENUM('Lunch','Breakfast','Dinner','Snack')
    protein FLOAT,
    carbs FLOAT,
    fat FLOAT, 
    fiber FLOAT,
    sodium FLOAT,
    potassium FLOAT,
    calcium FLOAT,
    phosphorus FLOAT,
    vitamin_A FLOAT,
    vitamin_B FLOAT,
    vitamin_C FLOAT,
    vitamin_D FLOAT,
    veg VARCHAR(10) CHECK (veg IN ('Yes', 'No'))
);


INSERT INTO meal_info (m_id, meal_name, protein, carbs, fat, fiber, sodium, potassium, calcium, phosphorus, vitamin_A, vitamin_B, vitamin_C, vitamin_D, veg) VALUES
(1, 'Moong Dal Khichdi', 14.0, 40.0, 3.0, 6.0, 250.0, 350.0, 60.0, 180.0, 9.0, 1.2, 8.0, 0.0, 'Yes'),
(2, 'Sprout Salad', 12.0, 20.0, 2.0, 7.5, 180.0, 400.0, 50.0, 140.0, 8.5, 1.0, 12.0, 0.0, 'Yes'),
(3, 'Grilled Chicken Tikka', 28.0, 5.0, 6.0, 2.0, 300.0, 350.0, 70.0, 250.0, 7.0, 0.9, 3.0, 0.3, 'No'),
(4, 'Palak Paneer', 18.0, 12.0, 10.0, 4.5, 350.0, 400.0, 250.0, 190.0, 14.0, 1.2, 18.0, 0.0, 'Yes'),
(5, 'Rajma Brown Rice', 16.0, 50.0, 4.0, 9.0, 300.0, 450.0, 85.0, 210.0, 7.0, 1.4, 11.0, 0.0, 'Yes'),
(6, 'Multigrain Roti', 6.0, 35.0, 2.5, 5.0, 150.0, 200.0, 40.0, 100.0, 6.0, 0.8, 4.0, 0.0, 'Yes'),
(7, 'Vegetable Upma', 8.0, 42.0, 5.0, 5.5, 200.0, 250.0, 60.0, 130.0, 7.5, 1.0, 9.0, 0.0, 'Yes'),
(8, 'Fish Curry', 25.0, 10.0, 8.0, 3.0, 320.0, 300.0, 90.0, 240.0, 6.5, 0.7, 4.0, 2.5, 'No'),
(9, 'Chickpea Chaat', 14.0, 45.0, 4.5, 7.5, 280.0, 350.0, 65.0, 170.0, 7.0, 1.1, 10.0, 0.0, 'Yes'),
(10, 'Methi Thepla', 9.0, 38.0, 6.0, 4.0, 200.0, 220.0, 55.0, 160.0, 8.0, 1.0, 5.5, 0.0, 'Yes');


Create Table meal_plan(plan_id AUTO_INCREMENT int primary,
u_id int ,
 day ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') ,
 breakfast_id int ,
lunch_id int,
  dinner_id int,
  FOREIGN KEY (u_id) references users(u_id),
  FOREIGN KEY (breakfast_id) references meal_info(m_id),
  FOREIGN KEY (lunch_id) references meal_info(m_id),
  FOREIGN KEY (dinner_id) references meal_info(m_id),
 
  veg varchar(10) CHECK(veg IN('YES' , 'NO')) );
