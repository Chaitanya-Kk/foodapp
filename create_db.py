from app import app, db

# Create the database within an application context
with app.app_context():
    db.create_all()
    print("Database created successfully!")
