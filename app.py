from flask import Flask, render_template, request, jsonify
import joblib
import os
import numpy as np

app = Flask(__name__)

# Load model data if exists
MODEL_PATH = 'model.pkl'

def get_model_data():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/foods', methods=['GET'])
def get_foods():
    model_data = get_model_data()
    if not model_data:
        return jsonify({"error": "Model not trained yet."}), 500
    
    foods = model_data.get('foods', [])
    model = model_data.get('model')
    
    # Send calories per 100g to frontend (which is coeff * 100)
    coefs = model.coef_
    food_list = [{"name": f, "cals": round(coefs[i] * 100, 1)} for i, f in enumerate(foods)]
    
    return jsonify({"foods": food_list})

@app.route('/api/predict', methods=['POST'])
def predict_calories():
    """
    Predict calories using the trained linear regression model.
    Expected JSON: { "items": [{"food": "Roti", "quantity": 100}, ...] }
    """
    model_data = get_model_data()
    if not model_data:
        return jsonify({"error": "Model not trained yet."}), 500
    
    model = model_data['model']
    foods = model_data['foods']
    food_to_idx = {f: i for i, f in enumerate(foods)}
    
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({"error": "No items provided."}), 400
    
    # We will calculate total by summing individual predictions,
    # or by passing in a single feature vector of all quantities.
    # Linear Regression is additive, so single feature vector is perfect.
    feature_vec = np.zeros(len(foods))
    item_breakdown = []
    
    for item in items:
        food_name = item.get('food')
        qty = float(item.get('quantity', 0))
        
        if food_name in food_to_idx:
            idx = food_to_idx[food_name]
            feature_vec[idx] += qty
            
            # Predict for individual item just to show breakdown
            single_vec = np.zeros(len(foods))
            single_vec[idx] = qty
            cal = float(model.predict([single_vec])[0])
            item_breakdown.append({
                "food": food_name,
                "quantity": qty,
                "calories": round(cal, 2)
            })
    
    total_calories = float(model.predict([feature_vec])[0])
    
    return jsonify({
        "total_calories": round(total_calories, 2),
        "breakdown": item_breakdown
    })

@app.route('/api/bmi', methods=['POST'])
def calculate_bmi():
    """
    Calculate BMI, categorization, and BMR / daily calorie recommendation.
    Expected JSON:
    {
        "height_cm": 170,
        "weight_kg": 70,
        "age_years": 25,
        "gender": "male"
    }
    """
    data = request.json
    try:
        height = float(data.get('height_cm'))
        weight = float(data.get('weight_kg'))
        age = float(data.get('age_years'))
        gender = data.get('gender', 'male').lower()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input parameters"}), 400
        
    if height <= 0 or weight <= 0 or age <= 0:
         return jsonify({"error": "Height, weight and age must be > 0"}), 400

    # BMI = weight / (height/100)^2
    bmi = weight / ((height / 100) ** 2)
    
    # Categorize
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    # Mifflin-St Jeor Equation for BMR
    if gender == 'female':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        
    # Add an active multiplier for recommended intake (Assume Moderately Active for general recommendation)
    recommended_intake = bmr * 1.55 
    
    return jsonify({
        "bmi": round(bmi, 2),
        "category": category,
        "bmr": round(bmr, 2),
        "recommended_calories": round(recommended_intake, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
