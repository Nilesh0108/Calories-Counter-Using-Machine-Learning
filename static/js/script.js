let appState = {
    meals: [],
    totalCalories: 0,
    dailyGoal: null,
    profile: null,
    availableFoods: [],
    burnerStats: { totalSteps: 0, totalKm: 0.0 }
};

// DOM Elements
const elements = {
    foodSelect: document.getElementById('foodItem'),
    foodOptions: document.getElementById('foodOptions'),
    foodForm: document.getElementById('foodForm'),
    qtyInput: document.getElementById('quantity'),
    foodUnit: document.getElementById('foodUnit'),
    mealList: document.getElementById('mealList'),
    itemCount: document.getElementById('itemCount'),
    totalCals: document.getElementById('totalCalories'),
    remainingCals: document.getElementById('remainingCalories'),
    progressFill: document.getElementById('progressFill'),
    healthMsg: document.getElementById('healthSuggestion'),
    
    bmiForm: document.getElementById('bmiForm'),
    bmiResult: document.getElementById('bmiResult'),
    bmiValue: document.getElementById('bmiValue'),
    bmiCategory: document.getElementById('bmiCategory'),
    recommendedGoal: document.getElementById('recommendedGoal'),
    
    resetBtn: document.getElementById('resetApp'),
    
    // Burner Modal Elements
    openBurnerBtn: document.getElementById('openBurnerBtn'),
    closeBurnerBtn: document.getElementById('closeBurnerBtn'),
    burnerModal: document.getElementById('burnerModal'),
    burnerForm: document.getElementById('burnerForm'),
    activityValue: document.getElementById('activityValue'),
    activityType: document.getElementById('activityType'),
    totalSteps: document.getElementById('totalSteps'),
    totalKm: document.getElementById('totalKm')
};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    loadState();
    if (!appState.burnerStats) appState.burnerStats = { totalSteps: 0, totalKm: 0.0 };
    fetchFoods();
    updateUI();
    updateBurnerUI();
});

// Fetch Foods from Backend and populate Dropdown
async function fetchFoods() {
    try {
        const response = await fetch('/api/foods');
        if (!response.ok) throw new Error("Failed to fetch foods");
        const data = await response.json();
        
        appState.availableFoods = data.foods;
        elements.foodOptions.innerHTML = '';
        data.foods.forEach(foodObj => {
            const option = document.createElement('option');
            option.value = foodObj.name;
            option.textContent = `~${foodObj.cals} kcal/100g`;
            elements.foodOptions.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading foods:", error);
    }
}

// BMI API Call
elements.bmiForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const payload = {
        age_years: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        height_cm: parseFloat(document.getElementById('height').value),
        weight_kg: parseFloat(document.getElementById('weight').value)
    };
    
    try {
        const response = await fetch('/api/bmi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error("Failed to calculate BMI");
        
        const result = await response.json();
        
        appState.profile = payload;
        appState.dailyGoal = result.recommended_calories;
        
        // Update BMI UI
        elements.bmiResult.classList.remove('hidden');
        elements.bmiValue.textContent = result.bmi;
        elements.bmiCategory.textContent = result.category;
        elements.recommendedGoal.textContent = result.recommended_calories + ' kcal';
        
        // Setup Bage Color
        elements.bmiCategory.className = 'badge';
        if(result.category.includes('Normal')) elements.bmiCategory.classList.add('success');
        else if (result.category.includes('Underweight')) elements.bmiCategory.classList.add('warning');
        else elements.bmiCategory.classList.add('danger');
        
        saveState();
        updateUI();
        
    } catch (error) {
        console.error("BMI calculation error:", error);
        alert("Error calculating BMI. Check inputs and server connection.");
    }
});

// Add Food API Call
elements.foodForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const food = elements.foodSelect.value;
    const qty = parseFloat(elements.qtyInput.value);
    const unit = elements.foodUnit.value;
    
    if(!food || qty <= 0) return;
    
    // Add temporarily
    const tempItem = { id: Date.now(), food, quantity: qty, unit: unit };
    appState.meals.push(tempItem);
    
    // Recalculate whole list via API
    await recalculateCalories();
    
    // Reset Form
    elements.qtyInput.value = '';
    elements.foodSelect.value = '';
});

// Auto-select unit based on food name
elements.foodSelect.addEventListener('input', (e) => {
    const foodName = e.target.value;
    const isDrink = /tea|coffee|juice|milk|soda|cola|drink|buttermilk|lassi|lemonade|water|beer|wine|smoothie|shake/i.test(foodName);
    elements.foodUnit.value = isDrink ? 'ml' : 'g';
});

// Remove Food
window.removeMeal = async (id) => {
    appState.meals = appState.meals.filter(m => m.id !== id);
    await recalculateCalories();
};

// API Call to predict calories based on ML model
async function recalculateCalories() {
    if(appState.meals.length === 0) {
        appState.totalCalories = 0;
        saveState();
        updateUI();
        return;
    }
    
    try {
        // Prepare API payload for ML Model prediction
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items: appState.meals })
        });
        
        if (!response.ok) throw new Error("Prediction API failed");
        
        const data = await response.json();
        
        appState.totalCalories = data.total_calories;
        
        // Enhance our meal array with returned individual calories
        data.breakdown.forEach((bItem, i) => {
            // Because ML retains order, we match by index
            if(appState.meals[i]) {
                appState.meals[i].calories = bItem.calories;
            }
        });
        
        saveState();
        updateUI();
        
    } catch (error) {
        console.error("Error recalcing calories:", error);
    }
}

// Main UI Update Function
function updateUI() {
    // 1. Update Progress Bar & Stats
    elements.totalCals.textContent = appState.totalCalories;
    
    if (appState.dailyGoal) {
        const left = appState.dailyGoal - appState.totalCalories;
        elements.remainingCals.textContent = Math.round(left > 0 ? left : 0);
        
        let percent = (appState.totalCalories / appState.dailyGoal) * 100;
        if(percent > 100) percent = 100;
        
        elements.progressFill.style.width = percent + '%';
        
        // Progress Color based on health logic
        if(appState.totalCalories > appState.dailyGoal) {
            elements.progressFill.style.background = 'var(--danger)';
            elements.healthMsg.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color:var(--danger)"></i> You are exceeding your daily calorie limit.';
        } else if (appState.totalCalories > appState.dailyGoal * 0.8) {
            elements.progressFill.style.background = 'var(--success)';
            elements.healthMsg.innerHTML = '<i class="fa-solid fa-check-circle" style="color:var(--success)"></i> Your diet is balanced.';
        } else {
            elements.progressFill.style.background = 'linear-gradient(90deg, var(--accent-orange), var(--accent-red))';
            elements.healthMsg.innerHTML = '<i class="fa-solid fa-bell" style="color:var(--accent-orange)"></i> You need to eat more to reach your goal.';
        }
    } else {
        elements.remainingCals.textContent = '--';
        elements.progressFill.style.width = '0%';
        elements.healthMsg.textContent = 'Please calculate your BMI to get personalized goals.';
    }
    
    // 2. Render List
    elements.itemCount.textContent = appState.meals.length + ' item' + (appState.meals.length !== 1 ? 's' : '');
    
    if(appState.meals.length === 0) {
        elements.mealList.innerHTML = '<li class="empty-state">No meals added yet. Let\'s eat!</li>';
    } else {
        elements.mealList.innerHTML = '';
        appState.meals.slice().reverse().forEach(meal => {
            // Fallback for old localstorage data, otherwise use stored unit
            const isDrink = /tea|coffee|juice|milk|soda|cola|drink|buttermilk|lassi|lemonade|water|beer|wine|smoothie|shake/i.test(meal.food);
            const unit = meal.unit ? meal.unit : (isDrink ? 'ml' : 'g');
            
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="meal-info">
                    <span class="meal-name">${meal.food}</span>
                    <span class="meal-qty">${meal.quantity} ${unit}</span>
                </div>
                <div style="display:flex; align-items:center; gap: 15px;">
                    <span class="meal-cal">${meal.calories ? meal.calories + ' kcal' : '...'}</span>
                    <button class="btn-remove" onclick="removeMeal(${meal.id})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            `;
            elements.mealList.appendChild(li);
        });
    }
}

// Reset App
elements.resetBtn.addEventListener('click', () => {
    if(confirm('Are you sure you want to reset today\'s meals?')) {
        appState.meals = [];
        appState.totalCalories = 0;
        recalculateCalories(); // updates UI
    }
});

// --- Calorie Burner Modal Logic ---
elements.openBurnerBtn.addEventListener('click', () => {
    elements.burnerModal.classList.add('active');
});

elements.closeBurnerBtn.addEventListener('click', () => {
    elements.burnerModal.classList.remove('active');
});

elements.burnerModal.addEventListener('click', (e) => {
    if (e.target === elements.burnerModal) {
        elements.burnerModal.classList.remove('active');
    }
});

elements.burnerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const value = parseFloat(elements.activityValue.value);
    const type = elements.activityType.value;
    
    if (isNaN(value) || value <= 0) return;
    
    if (!appState.burnerStats) appState.burnerStats = { totalSteps: 0, totalKm: 0.0 };
    
    if (type === 'steps') {
        appState.burnerStats.totalSteps += value;
    } else {
        appState.burnerStats.totalKm += value;
    }
    
    elements.activityValue.value = '';
    saveState();
    updateBurnerUI();
});

function updateBurnerUI() {
    if (!appState.burnerStats) return;
    elements.totalSteps.textContent = appState.burnerStats.totalSteps;
    // Format to 2 decimal places if it's not a whole number
    elements.totalKm.textContent = Number.isInteger(appState.burnerStats.totalKm) ? 
        appState.burnerStats.totalKm : 
        appState.burnerStats.totalKm.toFixed(2);
}

// LocalStorage Persistence
function saveState() {
    localStorage.setItem('calorieAppState', JSON.stringify(appState));
}

function loadState() {
    const saved = localStorage.getItem('calorieAppState');
    if (saved) {
        try {
            appState = JSON.parse(saved);
            
            // Restore Profile if exists
            if(appState.profile) {
                document.getElementById('age').value = appState.profile.age_years;
                document.getElementById('gender').value = appState.profile.gender;
                document.getElementById('height').value = appState.profile.height_cm;
                document.getElementById('weight').value = appState.profile.weight_kg;
                // re-calc BMI silently to restore badges state
                elements.bmiForm.dispatchEvent(new Event('submit'));
            }
        } catch (e) {
            console.error("Failed to load local state", e);
        }
    }
}
