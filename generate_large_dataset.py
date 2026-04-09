import pandas as pd
import random

# Existing defaults to keep
existing_foods = {
    "Roti": 297, "Rice": 130, "Dal": 116, "Paneer": 296, "Samosa": 262,
    "Dosa": 168, "Poha": 180, "Pani Puri": 220, "Vada Pav": 300, 
    "Pav Bhaji": 150, "Burger": 295, "Pizza": 266, "Fries": 312, 
    "Noodles": 138, "Fried Rice": 163, "Manchurian": 180, "Spring Rolls": 250
}

data = []
for name, cal in existing_foods.items():
    data.append({"Food_Item": name, "Calories_per_100g": cal})

# Helpers for generation
def generate_items(bases, styles, modifiers, base_cals):
    for base in bases:
        for style in styles:
            for mod in modifiers:
                name = f"{mod} {base} {style}".strip()
                # random variance around the base calories
                cal = int(base_cals[base] * random.uniform(0.8, 1.3))
                data.append({"Food_Item": name, "Calories_per_100g": cal})

# 1. Non-Veg (Combinations)
non_veg_bases = {"Chicken": 239, "Mutton": 294, "Fish": 206, "Egg": 155, "Prawn": 99, "Beef": 250, "Pork": 242}
non_veg_styles = ["Curry", "Masala", "Fry", "Tikka", "Biryani", "Korma", "Roast", "Grilled", "Keema", "Vindaloo", "Bhuna"]
non_veg_mods = ["Spicy", "Mild", "Butter", "Garlic", "Homestyle", "Restaurant Style"]

generate_items(non_veg_bases.keys(), non_veg_styles, non_veg_mods, non_veg_bases)

# 2. Veg / Indian Bhaji
veg_bases = {"Aloo": 89, "Paneer": 296, "Bhindi": 33, "Gobi": 25, "Matar": 81, "Chana": 164, "Palak": 23, "Mushroom": 22, "Baingan": 24, "Tofu": 144, "Rajma": 127}
veg_styles = ["Masala", "Fry", "Curry", "Makhanwala", "Bhurji", "Tikka", "Kofta", "Do Pyaza", "Sabzi"]
veg_mods = ["Dry", "Gravy", "Spicy", "Mild", "Dhaba Style", "Jain"]

generate_items(veg_bases.keys(), veg_styles, veg_mods, veg_bases)

# 3. Fruits
fruit_bases = {"Apple": 52, "Banana": 89, "Mango": 60, "Orange": 47, "Grapes": 69, "Papaya": 43, "Watermelon": 30, "Pineapple": 50, "Guava": 68, "Pomegranate": 83, "Strawberry": 32, "Melon": 34, "Kiwi": 61, "Pear": 57}
fruit_styles = ["Fresh", "Juice", "Shake", "Dried", "Salad"]
fruit_mods = [""]

# adjust calories based on style
for base in fruit_bases.keys():
    for style in fruit_styles:
        name = f"{style} {base}".strip()
        cal = fruit_bases[base]
        if style == "Dried": cal *= 4
        elif style == "Shake": cal = int(cal * 1.5 + 50)
        elif style == "Juice": cal = int(cal * 0.9)
        data.append({"Food_Item": name, "Calories_per_100g": cal})

# 4. Snacks / Street Food
snack_bases = {"Samosa": 262, "Kachori": 400, "Pakora": 250, "Dosa": 168, "Idli": 58, "Vada": 280, "Puri": 320, "Paratha": 300, "Kulcha": 270, "Roll": 250, "Momos": 150}
snack_styles = [""]
snack_mods = ["Aloo", "Paneer", "Onion", "Mix Veg", "Cheese", "Chicken", "Egg", "Mutton", "Soya"]

for base in snack_bases.keys():
    for mod in snack_mods:
        name = f"{mod} {base}".strip()
        cal = snack_bases[base]
        if mod == "Cheese" or mod == "Paneer": cal = int(cal * 1.2)
        elif mod == "Chicken" or mod == "Mutton": cal = int(cal * 1.1)
        data.append({"Food_Item": name, "Calories_per_100g": cal})

# 5. Fast Food
ff_bases = {"Burger": 295, "Pizza": 266, "Sandwich": 250, "Pasta": 131, "Wrap": 200, "Salad": 100}
ff_styles = [""]
ff_mods = ["Veg", "Cheese", "Chicken", "Paneer", "Mushroom", "Tandoori", "BBQ", "Mexican"]

for base in ff_bases.keys():
    for mod in ff_mods:
        name = f"{mod} {base}".strip()
        cal = ff_bases[base]
        if mod == "Cheese": cal += 50
        data.append({"Food_Item": name, "Calories_per_100g": cal})

# 6. Sweets / Desserts
sweet_bases = {"Gulab Jamun": 300, "Rasgulla": 186, "Barfi": 350, "Halwa": 300, "Kheer": 110, "Ladoo": 400, "Peda": 370, "Ice Cream": 207, "Cake": 350, "Pastry": 390}
sweet_styles = [""]
sweet_mods = ["Kesar", "Pista", "Chocolate", "Vanilla", "Mango", "Almond", "Special", "Reduced Sugar"]

for base in sweet_bases.keys():
    for mod in sweet_mods:
        name = f"{mod} {base}".strip()
        cal = sweet_bases[base]
        if mod == "Chocolate": cal += 40
        elif mod == "Reduced Sugar": cal = int(cal * 0.7)
        data.append({"Food_Item": name, "Calories_per_100g": cal})

# 7. Drinks and Beverages
drink_bases = {"Tea": 1, "Coffee": 2, "Milk": 42, "Juice": 45, "Soda": 41, "Cola": 43, "Energy Drink": 45, "Buttermilk": 40, "Lassi": 75, "Lemonade": 25, "Coconut Water": 19, "Beer": 43, "Wine": 83, "Smoothie": 60, "Milkshake": 110, "Hot Chocolate": 77}
drink_styles = ["Regular", "Iced", "Cold", "Hot", "Diet", "Sugar-Free", "Premium", "Fresh"]
drink_mods = ["Sweet", "Black", "Green", "Lemon", "Masala", "Ginger", "Apple", "Orange", "Mango", "Mixed Fruit", "Mint", ""]

for base in drink_bases.keys():
    for style in drink_styles:
        for mod in drink_mods:
            name = f"{style} {mod} {base}".strip()
            # Clean up double spaces
            name = " ".join(name.split())
            cal = drink_bases[base]
            
            if "Diet" in style or "Sugar-Free" in style:
                if base in ["Soda", "Cola", "Energy Drink", "Lemonade"]:
                    cal = int(cal * 0.05) # almost zero cal
                else:
                    cal = int(cal * 0.5) # reduced cal
            elif "Milkshake" in base or "Lassi" in base or "Smoothie" in base:
                if "Mango" in mod or "Sweet" in mod:
                    cal = int(cal * 1.3)
                    
            if base in ["Tea", "Coffee"]:
                if "Sweet" in mod and "Black" not in mod:
                    cal += 30 # sugar + milk
                elif "Black" in mod or "Green" in mod:
                    cal = 2 # minimal calories
                    
            data.append({"Food_Item": name, "Calories_per_100g": cal})

# Ensure uniqueness
df = pd.DataFrame(data)
df = df.drop_duplicates(subset=["Food_Item"])
print(f"Generated {len(df)} discrete food combinations!")

# Sample down or pad to exactly/above 1000 if needed, but we definitely have above 1000.
# Let's write to csv
df.to_csv("food_data.csv", index=False)
print("Saved to food_data.csv")
