from marshmallow import Schema, fields, validate, ValidationError, post_load

def get_age_range(age: int):
    if 18 <= age <= 24:
        return "18-24"
    elif 25 <= age <= 35:
        return "25-35"
    elif 36 <= age <= 40:
        return "36-40"
    elif 41 <= age <= 45:
        return "41-45"
    elif 46 <= age <= 50:
        return "46-50"
    elif 51 <= age <= 55:
        return "51-55"
    elif 56 <= age <= 60:
        return "56-60"
    elif 61 <= age <= 65:
        return "61-65"
    elif 66 <= age <= 70:
        return "66-70"
    elif 71 <= age <= 75:
        return "71-75"
    elif 76 <= age <= 99:
        return "76-99"
    else:
        return "Invalid age"


def premium_breakout(user_data, primary, secondary=None):
    try:
        premium = []
        if user_data["adults"] > 1:
            individual = list(filter(lambda primary: primary['members'] == "1a", primary))[0]
            group = list(filter(lambda primary: primary['members'] != "1a", primary))[0]
                
            for sum_assured in group:
                if sum_assured not in ["members", "city_tier", "age_range"]:
                    
                    if user_data["children"] > 0:
                        
                        adult_1 = individual[sum_assured]
                        adult_2 = secondary[sum_assured] * 0.5517
                        children = group[sum_assured] - (adult_1 + adult_2)
                        
                        children_premium = []
                        for i in range(1, user_data["children"] + 1):
                            children_premium.append({
                                    "user_type": f"child_{i}",
                                    "base_rate": (children * 2)/user_data["children"],
                                    "floater_discount": 50,
                                    "discounted_rate": children/user_data["children"]
                                })
                        
                        temp = {
                            "sum_assured": sum_assured,
                            "total": group[sum_assured],
                            "premium_breaks": [
                                {
                                    "user_type": "adult_1",
                                    "base_rate": adult_1,
                                    "floater_discount": 0,
                                    "discounted_rate": adult_1
                                },
                                {
                                    "user_type": "adult_2",
                                    "base_rate": secondary[sum_assured],
                                    "floater_discount": 45,
                                    "discounted_rate": adult_2
                                }
                            ]
                        }
                        temp["premium_breaks"].extend(children_premium)
                        premium.append(temp)
                        
                    else:
                        adult_1 = individual[sum_assured]
                        adult_2 = secondary[sum_assured] / 2
                        
                        premium.append({
                            "sum_assured": sum_assured,
                            "total": group[sum_assured],
                            "premium_breaks": [
                                {
                                    "user_type": "adult_1",
                                    "base_rate": adult_1,
                                    "floater_discount": 0,
                                    "discounted_rate": adult_1
                                },
                                {
                                    "user_type": "adult_2",
                                    "base_rate": adult_2 * 2,
                                    "floater_discount": 45,
                                    "discounted_rate": adult_1
                                }
                            ]
                        })
                
        else:
            individual = list(filter(lambda primary: primary['members'] == "1a", primary))[0]
            
            for sum_assured in individual:
                
                if sum_assured not in ["members", "city_tier", "age_range"]:
                        
                    if user_data["children"] > 0:
                        
                        group = list(filter(lambda primary: primary['members'] != "1a", primary))[0]
                        
                        adult_1 = individual[sum_assured]
                        children = group[sum_assured] - adult_1
                        children_premium = []
                        
                        for i in range(1, user_data["children"] + 1):
                            children_premium.append({
                                "user_type": f"child_{i}",
                                "base_rate": (children * 2)/user_data["children"],
                                "floater_discount": 50,
                                "discounted_rate": children/user_data["children"]
                            })
                        temp={
                            "sum_assured": sum_assured,
                            "total": group[sum_assured],
                            "premium_breaks": [
                                {
                                    "user_type": "adult_1",
                                    "base_rate": adult_1,
                                    "floater_discount": 0,
                                    "discounted_rate": adult_1
                                }
                            ]
                        }
                        temp["premium_breaks"].extend(children_premium)
                        premium.append(temp)
                    else:
                        adult_1 = individual[sum_assured]
                        
                        premium.append({
                            "sum_assured": sum_assured,
                            "total": adult_1,
                            "premium_breaks": [
                                {
                                    "user_type": "adult_1",
                                    "base_rate": adult_1,
                                    "floater_discount": 0,
                                    "discounted_rate": adult_1
                                }
                            ]
                        })
        return premium
    except Exception as e:
        print(e)


class PremiumDataSchema(Schema):
    adults = fields.Integer(required=True, validate=validate.Range(min=1, max=2))
    children = fields.Integer(required=True, validate=validate.Range(min=0, max=4))
    city = fields.String(required=True, validate=validate.Length(min=1))
    ages = fields.Dict(required=True)

    @staticmethod
    def validate_ages(data):
        for key, value in data.items():
            if key.endswith('a') and not (18 <= value <= 99):
                raise ValidationError(f"Age for key '{key}' must be between 18 and 99")
            elif key.endswith('c') and not (1 <= value <= 17):
                raise ValidationError(f"Age for key '{key}' must be between 1 and 17")

    @post_load
    def validate_input(self, data, **kwargs):
        self.validate_ages(data['ages'])