def calculate_bmi(weight: float, height: float) -> float:
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def get_bmi_category(weight: float, height: float) -> str:
    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)
    return f"Your BMI is {bmi}. Category: {category}"