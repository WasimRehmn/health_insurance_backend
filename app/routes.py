from flask import request, jsonify
from marshmallow import  ValidationError
from app import app, mongo
from app.model import get_age_range, premium_breakout, PremiumDataSchema

@app.route("/premium", methods=["POST"])
def calculate_premium():
    data = request.json
    
    schema = PremiumDataSchema()

    try:
        result = schema.load(data)
    except ValidationError as e:
        return jsonify({"error": f"Validation failed: {e.messages}"}), 400

    
    try:
        adult_ages = [data['ages'][f"{i}a"] for i in range(1, data['adults'] + 1)]

        query = {
            "members": { "$in" : ["1a", f"{data['adults']}a"] if data['children'] == 0 else ["1a", f"{data['adults']}a,{data['children']}c"]},
            "age_range": get_age_range(max(adult_ages))
        }
        
        premium_collection = mongo.db.premium_rates
        
        primary_premium = list(premium_collection.find(query, {'_id': 0}))
        secondry_premium = None
        if data['adults'] > 1:
            secondry_premium = dict(premium_collection.find_one({"members": "1a", "age_range": get_age_range(min(adult_ages))}, {'_id': 0}))
        
        premium = premium_breakout(data, primary_premium, secondry_premium)
        
        return jsonify({"initial_sum_assured": "500000", "premium": premium}), 200
    except Exception as e:
        return jsonify({"error": f"Server Error: {e}"}), 500

# Define other routes as needed
