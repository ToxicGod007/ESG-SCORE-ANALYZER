import sys
import json
import joblib
import pandas as pd

# Load the model file provided by your friend
# Ensure the path matches where you saved the .pkl file
try:
    model = joblib.load('backend/scripts/esg_model.pkl')
except Exception as e:
    # If the model fails to load, Node.js will catch this error
    print(json.dumps({"error": f"Model load failed: {str(e)}"}))
    sys.exit(1)

def run_analysis():
    # Read the data sent from Node.js (index.ejs form)
    input_json = sys.stdin.read()
    if not input_json:
        return
    
    data = json.loads(input_json)

    # Prepare all 16 points for the ML Model
    # Note: Ensure the order below matches your friend's training order
    features = pd.DataFrame([{
        "industry_type": data.get('industry'),                  # 1
        "annual_revenue": float(data.get('revenue', 0)),        # 2
        "total_employees": int(data.get('total_employees', 0)),  # 3
        "energy_consumption": float(data.get('energy_kwh', 0)), # 4
        "renewable_usage": float(data.get('renewable_kwh', 0)), # 5
        "water_consumption": float(data.get('water_liters', 0)),# 6
        "waste_generated": float(data.get('waste_kg', 0)),      # 7
        "waste_recycled": float(data.get('recycled_kg', 0)),    # 8
        "female_employees": int(data.get('female_employees', 0)),# 9
        "disabled_employees": int(data.get('disabled_employees', 0)), # 10
        "safety_accidents": int(data.get('accidents', 0)),      # 11
        "employees_trained": int(data.get('trained_count', 0)), # 12
        "harassment_complaints": int(data.get('complaints', 0)),# 13
        "sustainability_committee": 1 if data.get('committee') == 'Yes' else 0, # 14 (Numeric)
        "regulatory_fines": float(data.get('fines', 0)),        # 15
        "policies_count": len(data.get('policies', []))         # 16 (Numeric count)
    }])

    try:
        # Generate the prediction
        prediction = model.predict(features)[0]

        # Send JSON back to Node.js
        # ONLY print the JSON object
        output = {
            "totalEsgScore": round(float(prediction), 2),
            "aiAnalysis": [
                f"Analysis based on {features['policies_count'][0]} active policies.",
                "High regulatory fines impacted the score." if features['regulatory_fines'][0] > 0 else "Excellent compliance record.",
                "Focus on increasing renewable energy ratio for better results."
            ]
        }
        print(json.dumps(output))

    except Exception as e:
        print(json.dumps({"error": f"Prediction failed: {str(e)}"}))

if __name__ == "__main__":
    run_analysis()
