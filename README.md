# CalorieTracker - Intelligent Meal Tracking & Health Engine

![CalorieTracker Preview](https://img.shields.io/badge/Status-Active-success) ![Machine Learning](https://img.shields.io/badge/ML-Linear_Regression-blue) ![Python](https://img.shields.io/badge/Backend-Flask-yellow)

## 🌟 Overview
CalorieTracker is a comprehensive, modern web application designed to help users intelligently track their daily calorie intake and activity. Designed with a sleek, responsive dark-mode UI, it behaves dynamically on desktops and smoothly transitions to a native-app-like experience on mobile devices. 

It calculates your Body Mass Index (BMI), provides an intelligent daily calorie goal using the Mifflin-St Jeor equation, tracks your food intake via a custom Machine Learning engine, and keeps you active with built-in Step/KM tracking and guided mobility exercises.

## 🚀 Features
- **BMI & Smart Goals**: Generates personalized daily calorie intake goals based on Age, Gender, Height, and Weight.
- **ML Calorie Prediction Engine**: Forget static databases; our scikit-learn Machine Learning backend estimates exact calories from a vast subset of custom inputs.
- **Calorie Burner Module**: Built-in widget to track Steps and KMs, complete with a beautifully laid out 15-20 minute simple mobility exercise routine.
- **Premium UI / UX**: Employs Glassmorphism, dynamic gradients, CSS Grid layouts, Font-Awesome icons, and zero-stutter micro-animations.
- **Progressive Web App UX**: Meta-tags optimized so you can add this site to your Mobile Home Screen for a seamless, app-like, distraction-free environment.

## 💻 Tech Stack
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Modern Flexbox/Grid)
- **Backend / API**: Python, Flask
- **Machine Learning**: `scikit-learn` (Linear Regression), `numpy`, `joblib`

## ⚙️ How it Works & Installation
1. Install project dependencies via the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure you have a food dataset and have trained your model (this creates `model.pkl`):
   ```bash
   python train_model.py
   ```
3. Run the Flask Web Server:
   ```bash
   python app.py
   ```
4. Access the App: Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🧠 Machine Learning Algorithm Used

We employ a custom machine learning approach to actively predict and extrapolate calorie impacts rather than relying solely on arbitrary lookups. 

Here is a quick breakdown to understand the model:

📊 **"Why & How does it work?"**
Say in very simple words:
> "Linear Regression model from scikit-learn to predict calories based on food type and quantity. Because our output is a numeric value (calories), and Linear Regression is highly suitable for accurately predicting continuous numerical values. The model learns the relationship between food quantity and calories from the dataset. Then it uses that relationship to predict calories for new inputs."

🔍 **"What are inputs and outputs?"**
Say:
> **Input**: Food name + quantity
> **Output**: Calories

⚡ **One-Line Smart Answer (Best 🔥)**
> "Linear Regression finds a mathematical relationship between our input (food and quantity) and output (calories) to make predictions."

---
*Created with ❤️ for intelligent health tracking.*
