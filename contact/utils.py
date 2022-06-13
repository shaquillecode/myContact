"""Utils.py"""
from . import constants as csts

def remove_punctuations(test_str):
    """Removes punctuations from string"""
    if isinstance(test_str, str):
        for char in test_str:
            if char in csts.PUNC:
                test_str = test_str.replace(char, "")
        return test_str

def zip_validator(zipcode):
    """Checks if Zip code is in a valid Zip Code Format"""
    res = None
    if len(zipcode) < 5:
        res = False
    else:
        if len(zipcode) == 5 and zipcode.isnumeric():
            res = True
        else:
            if len(zipcode) > 5 and '-' in zipcode:
                zipcode = zipcode.split('-')
                if len(zipcode[0]) == 5 and zipcode[0].isnumeric() and zipcode[1].isnumeric():
                    res = True
                else:
                    res = False
            else:
                res = False
    return res

def address_validator(result):
    """Checks if Address Format is in a valid Address Format"""

    address_name = remove_punctuations("".join(result["name"].split()))
    city = remove_punctuations("".join(result["city"].split()))
    state = remove_punctuations("".join(result["state"].split()))
    country = remove_punctuations("".join(result["country"].split()))


    for i in address_name:
        if not i.isalnum():
            print(f"{i} is not a address name")
            return False

    for i in city:
        if not i.isalpha():
            print(f"{i} is not a city")
            return False

    for i in state:
        if not i.isalpha():
            print(f"{i} is not a state")
            return False

    for i in country:
        if not i.isalpha():
            print(f"{i} is not a country")
            return False

    if not zip_validator(remove_punctuations(result["zip_code"])):
        print(f"{result['zip_code']} is not a valid Zip code")
        return False

    return True

def approx_coordinates(lat_, long_, decimal=5):
    """
    rounds latitude and longitude coordinates to a given decimal place
    default is 5.
    """
    return (round(lat_, decimal), round(long_, decimal))
