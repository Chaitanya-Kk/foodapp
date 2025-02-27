from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from models import User, MealPlan, FoodItem
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, MealPlanForm, BMICalculatorForm
from bmi_calculator import calculate_bmi, get_bmi_category
from food_recommender import recommend_food_permutations  

def init_routes(app):
    # Home Route
    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html")

    # About Route
    @app.route("/about")
    def about():
        return render_template("about.html")

    # Register Route
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    # Login Route
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("bmi"))
            else:
                flash("Login failed. Check email and password.", "danger")
        return render_template("login.html", form=form)

    # Logout Route
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("home"))

    # BMI Route
    @app.route("/bmi", methods=["GET", "POST"])
    def bmi():
        form = BMICalculatorForm()
        if form.validate_on_submit():
            weight = float(form.weight.data)
            height = float(form.height.data) / 100  # Convert cm to meters
            bmi_value = round(weight / (height ** 2), 2)
            bmi_category = get_bmi_category(bmi_value)

            # Get meal recommendations based on BMI category
            recommendations = recommend_food_items(bmi_category)

            # Store in session for use in meal plan page
            session["bmi"] = bmi_value
            session["category"] = bmi_category
            session["recommendations"] = recommendations

            return redirect(url_for("meal_plan_results"))  
        return render_template("bmi.html", form=form)

    # Meal Plan Results Page
    @app.route("/meal_plan_results")
    def meal_plan_results():
        bmi_value = session.get("bmi", "N/A")
        category = session.get("category", "N/A")
        recommendations = session.get("recommendations", [])

        return render_template(
            "meal_plan_results.html",
            bmi=bmi_value,
            category=category,
            recommendations=recommendations,
            meal_plan=recommendations  
        )

    # Meal Planning Route
    @app.route("/meal_plan", methods=["GET", "POST"])
    @login_required
    def meal_plan():
        form = MealPlanForm()
        if form.validate_on_submit():
            meal = MealPlan(content=form.content.data, user_id=current_user.id)
            db.session.add(meal)
            db.session.commit()
            flash("Meal plan saved!", "success")
            return redirect(url_for("meal_plan"))
        return render_template("meal_plan.html", form=form)

    # User Dashboard
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html", user=current_user)

    # User Account Page
    @app.route("/account")
    @login_required
    def account():
        return render_template("account.html", user=current_user)
