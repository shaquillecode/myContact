"""Utils.py"""
from . import constants as csts

def remove_punctuations(test_str):
    """Removes punctuations from string"""
    if isinstance(test_str, str):
        for char in test_str:
            if char in csts.PUNC:
                test_str = test_str.replace(char, "")
        return test_str

def street_name_validator(st_name):
    """Checks if Street name is in a valid Format"""
    alphanum = ""
    st_name = remove_punctuations("".join(st_name))
    for i, char in enumerate(st_name):
        if st_name[i].isnumeric():
            alphanum += st_name[i]
        if((st_name[i] >= 'A' and st_name[i] <= 'Z') or (st_name[i] >= 'a' and st_name[i] <= 'z')):
            alphanum += st_name[i]
    if alphanum != st_name:
        return False
    return True

def state_validator(state):
    """Checks if State exists in STATES dictionary"""
    if isinstance(state,str):
        do_exist = False
        for key,value in csts.STATES.items():
            if key == state.strip().upper() or value == state.strip().capitalize():
                do_exist = True
        return do_exist


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

def address_validator(address):
    """Checks if Address Format is in a valid Address Format"""
    street_address_value = address["street_address"].split()

    address_name = street_address_value[:-3]
    address_city = street_address_value[-3]
    address_state = street_address_value[-2]
    address_zip = street_address_value[-1]

    if not street_name_validator(address_name):
        print(f"{address_name} is not a street name")
        return False

    address_city = remove_punctuations(address_city)
    for i in address_city:
        if not i.isalpha():
            print(f"{i} is not a city")
            return False

    address_state = remove_punctuations(address_state)
    if not state_validator(address_state):
        print(f"{address_state} is not a valid State")
        return False

    if not zip_validator(remove_punctuations(address_zip)):
        print(f"{address_zip} is not a valid Zip code")
        return False

    return True

def approx_coordinates(lat_, long_, decimal=5):
    """
    rounds latitude and longitude coordinates to a given decimal place
    default is 5.
    """
    return (round(lat_, decimal), round(long_, decimal))
