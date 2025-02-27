def calculate_bmi(weight: float, height_cm: float) -> float:
    """Calculate BMI given weight in kg and height in cm."""
    height_m = height_cm / 100  # Convert cm to meters
    return round(weight / (height_m ** 2), 2)


def get_bmi_category(bmi: float) -> str:
    """Determine BMI category based on BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


# Example Usage
if __name__ == "__main__":
    weight = float(input("Enter weight in kg: "))
    height = float(input("Enter height in cm: "))
    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)
    print(f"BMI: {bmi}, Category: {category}")
