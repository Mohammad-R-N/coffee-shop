from kavenegar import *
import re
from django.core.exceptions import ValidationError
from django.db import models


def send_otp(phone_number, code):
    try:
        API_KEY = "35484F79694A68527A58302F43354176354C366A62552B37665942646F334439627179326F564E766E63413D"
        api = KavenegarAPI(f"https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json")
        params = {
            "sender": "",
            "receptor": phone_number,
            "token": code,
            "template": "maktab",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def phone_number_validator(value):
    """
    Validates phone numbers in the 09XX, 00989XX, or +98XX format and replaces the +98 and 0098 parts with 0.
    """
    phone_regex = r"^(\+98|0098|0)?9\d{9}$"
    if not re.match(phone_regex, value):
        raise ValidationError(
            "Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."
        )
    formatted_phone_number = re.sub(r"^\+98|^0098", "0", value)
    return formatted_phone_number
