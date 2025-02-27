import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('site.db')
cursor = conn.cursor()

# Create table for users
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    image_file TEXT NOT NULL DEFAULT 'default.jpg',
    password TEXT NOT NULL
)
''')

# Create table for food items
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    calories INTEGER NOT NULL,
    region TEXT NOT NULL,
    protein REAL NOT NULL,
    carbs REAL NOT NULL,
    fats REAL NOT NULL
)
''')

# Create table for meal plans
cursor.execute('''
CREATE TABLE IF NOT EXISTS meal_plan (
    id INTEGER PRIMARY KEY,
    date_posted TEXT NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

# Sample data for food items
food_data = [
    ('Apple', 95, 'North America', 0.3, 25, 0.2),
    ('Banana', 105, 'South America', 1.3, 27, 0.3),
    ('Rice', 206, 'Asia', 4.3, 45, 0.4),
    ('Bread', 79, 'Europe', 2.7, 15, 1),
    ('Pasta', 131, 'Europe', 5, 25, 1.1),
    ('Chicken', 335, 'North America', 31, 0, 19),
    ('Fish', 206, 'Asia', 22, 0, 12),
    ('Lentils', 230, 'Asia', 18, 39, 1),
    ('Beef', 250, 'North America', 26, 0, 15)
]

# Insert sample data into the table
cursor.executemany('''
INSERT INTO food_items (name, calories, region, protein, carbs, fats)
VALUES (?, ?, ?, ?, ?, ?)
''', food_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and populated with sample data.")