import json


def validate_signup(sign_up_info):
    for key, value in sign_up_info.items():
        if value.strip() == "":
            return json.dumps({"user_signed_up": False, "message": "There are missing fields"})
    if sign_up_info['password'] != sign_up_info['repeat_password']:
        return json.dumps({"user_signed_up": False, "message": "Passwords not matching"})
    if len(sign_up_info['password']) > 35:
        return json.dumps({"user_signed_up": False, "message": "Password must not be above 35 characters"})
    if '@' not in sign_up_info["email"] or '.com' not in sign_up_info["email"]:
        return json.dumps({"user_signed_up": False, "message": "Please enter only valid emails"})

