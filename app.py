from flask import Flask, request, render_template, jsonify
import pandas as pd
import pickle
import numpy as np

# Initialize the Flask app

app = Flask(__name__)

# Load the trained model and cleaned dataset
model = pickle.load(open('GradientBoost.pkl', 'rb'))
dfc = pd.read_csv('cleaned_car_df2.csv')

# Route for the home page
@app.route('/')
def home():
    companies = dfc['Company'].unique()
    fuel_types = dfc['Fuel'].unique()
    print("Homepage accessed")
    return render_template('index.html', companies=companies, fuel_types=fuel_types)

# Route to dynamically fetch models based on the selected company
@app.route('/get_models', methods=['POST'])
def get_models():
    company = request.json['company']
    models = dfc[dfc['Company'] == company]['Model'].unique()
    return jsonify({'models': list(models)})

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        user_data = {
            'Model': data['Model'],
            'km_driven': float(data['km_driven']),
            'Fuel': data['Fuel'],
            'Owner': data['Owner'],
            'Year': int(data['Year']),
            'Company': data['Company']
        }

        # Convert user input to DataFrame
        input_data = pd.DataFrame([user_data])

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        return jsonify({'prediction': round(predicted_price, 2)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)