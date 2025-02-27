import pandas as pd
import itertools

def recommend_food_permutations(bmi_category, region, csv_path):
    try:
        df = pd.read_csv(csv_path)

        # Filter by region & BMI category
        filtered_df = df[(df["Region"] == region) & (df["BMI_Category"] == bmi_category)]

        if filtered_df.empty:
            return []

        meal_options = {
            "Breakfast": filtered_df["Breakfast"].dropna().unique().tolist(),
            "Lunch": filtered_df["Lunch"].dropna().unique().tolist(),
            "Dinner": filtered_df["Dinner"].dropna().unique().tolist()
        }

        # Generate all meal plan permutations (max 5 to avoid overload)
        meal_plans = list(itertools.product(meal_options["Breakfast"], meal_options["Lunch"], meal_options["Dinner"]))[:5]

        return [
            {"Breakfast": plan[0], "Lunch": plan[1], "Dinner": plan[2]} for plan in meal_plans
        ]
    
    except Exception as e:
        print("Error in food recommender:", e)
        return []
