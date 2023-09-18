from flask import request, jsonify
from app import app, mongo
from app.model import get_age_range, premium_breakout

@app.route("/premium", methods=["GET"])
def calculate_premium():
    # data = request.json
    data = {
        'sum_assured': 5000000, 
        'adults': 1, 
        'children': 3, 
        'city': 'Delhi', 
        'ages': {"1a": 41, "2a": 35, "1c": 17, "2c": 15, "3c": 13}
    }
    
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
    
    return jsonify({"premium": premium})

# Define other routes as needed
