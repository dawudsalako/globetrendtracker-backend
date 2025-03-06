from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route("/", methods=["GET"])
def home():
    return "Welcome to Globetrend Tracker API!", 200

@app.route("/predict", methods=["GET"])
def predict():
    category = request.args.get("category")
    bill = request.args.get("bill")
    year = request.args.get("year")

    if not category or not bill or not year:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        bill = float(bill)
    except ValueError:
        return jsonify({"error": "Invalid bill amount"}), 400

    price_increase = {
        "Vegan": {"2030": 11.80, "2040": 31.59, "2050": 52.78},
        "Balanced": {"2030": 13.39, "2040": 34.44, "2050": 57.00},
        "Meat and Dairy Heavy": {"2030": 15.49, "2040": 38.25, "2050": 62.62},
        "Vegetarian": {"2030": 13.14, "2040": 33.48, "2050": 55.15},
    }

    if category not in price_increase or year not in price_increase[category]:
        return jsonify({"error": "Invalid category or year"}), 400

    increase = price_increase[category][year]
    new_bill = bill * (1 + increase / 100)

    return jsonify({
        "predictions": {
            "Vegan": round(bill * (1 + price_increase["Vegan"][year] / 100), 2),
            "Balanced": round(bill * (1 + price_increase["Balanced"][year] / 100), 2),
            "Meat and Dairy Heavy": round(bill * (1 + price_increase["Meat and Dairy Heavy"][year] / 100), 2),
            "Vegetarian": round(bill * (1 + price_increase["Vegetarian"][year] / 100), 2),
        },
        "selected_category": category,
        "selected_year": year
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
