from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Updated percentage-based price increases
PRICE_INCREASES = {
    "Vegan": {"2030": 1.118, "2040": 1.3159, "2050": 1.5278},
    "Balanced": {"2030": 1.1339, "2040": 1.3444, "2050": 1.57},
    "Keto": {"2030": 1.1549, "2040": 1.3825, "2050": 1.6262},
    "Vegetarian": {"2030": 1.1314, "2040": 1.3348, "2050": 1.5515}
}

@app.route("/")
def home():
    return "Grocery Price Predictor API is running!"

@app.route("/predict", methods=["GET"])
def predict():
    category = request.args.get("category")
    bill = request.args.get("bill")
    selected_year = request.args.get("year")

    if not category or not bill or not selected_year:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        bill = float(bill)
    except ValueError:
        return jsonify({"error": "Invalid bill amount"}), 400

    if selected_year not in ["2030", "2040", "2050"]:
        return jsonify({"error": "Invalid year"}), 400

    # Generate predictions for all categories in the selected year
    predictions = {
        cat: round(bill * PRICE_INCREASES[cat][selected_year], 2)
        for cat in PRICE_INCREASES
    }

    return jsonify({
        "predictions": predictions,
        "selected_category": category,
        "selected_year": selected_year
    })

if __name__ == "__main__":
    app.run(debug=True)