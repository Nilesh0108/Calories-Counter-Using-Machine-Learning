import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

def generate_synthetic_data(food_df, samples_per_food=5):
    foods = food_df['Food_Item'].tolist()
    calories_per_100g = food_df['Calories_per_100g'].tolist()
    
    X = []
    y = []
    
    for idx, food in enumerate(foods):
        cal_per_g = calories_per_100g[idx] / 100.0
        # Generate random quantities between 10g and 1000g
        quantities = np.random.uniform(10, 1000, samples_per_food)
        for q in quantities:
            # Create feature vector where only the specific food's quantity is non-zero
            feature_vec = np.zeros(len(foods))
            feature_vec[idx] = q
            X.append(feature_vec)
            
            # The true calorie count
            y.append(q * cal_per_g)
            
    return np.array(X), np.array(y), foods

def main():
    print("Loading food data from food_data.csv...")
    try:
        food_df = pd.read_csv('food_data.csv')
    except Exception as e:
        print(f"Error reading food_data.csv: {e}")
        return
        
    print(f"Found {len(food_df)} food items. Generating synthetic dataset for ML...")
    X, y, food_names = generate_synthetic_data(food_df)
    
    print("Training Linear Regression model...")
    # fit_intercept=False because 0 quantity of all = 0 calories
    model = LinearRegression(fit_intercept=False)
    model.fit(X, y)
    
    print(f"Model trained! R^2 Score: {model.score(X, y)}")
    
    # Save the model and the food names to map future inputs
    model_data = {
        'model': model,
        'foods': food_names
    }
    joblib.dump(model_data, 'model.pkl')
    print("Model saved to model.pkl successfully.")

if __name__ == '__main__':
    main()
