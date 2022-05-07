'''Create your views here.'''
from pathlib import Path
import logging as logg
from django.shortcuts import render
import requests as rqs
from dotenv import dotenv_values
from . forms import FormInscription
from . models import Contact
from . import utils
from . import constants as csts


BASE_DIR = Path(__file__).resolve().parent.parent
config = dotenv_values(f"{BASE_DIR}/contact/.env")
logg.basicConfig(filename=csts.LOG_FILE,
level=logg.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def index(request):
    '''index'''
    res = "Apply for Brooklyn Nets Season Tickets here"
    msg = "Serious Inquiries only"
    return render(request, "index.html", {"res":res, "message":msg})

def login(request):
    '''Login Page'''
    form = FormInscription(request.POST)
    username = form["username"].value()
    password = form["password"].value()

    if isinstance(username,str) and isinstance(password, str):
        if username.strip() == 'my' and password.strip() == 'info':
            logg.info("Authenticated user")
            msg = 'Nice! Username and password was correct'
            return render(request, "info.html", {'message':msg})
    else:
        logg.info("Not Authenticated user")
        # count number of login attempts, block user from login
        msg = 'You will get blocked after 5 wrong attempts'
        return render(request, "login.html", {'message':msg})

def saved(request):
    '''This view will Display all saved contacts'''
    all_contacts = Contact.objects.all()
    return render(request,"saved.html", {"action":"Display all Contacts", "all_contacts":all_contacts})

def info(request):
    """
    Saves Clients/Users to Admin Site Contact book
    Admin will be able to add, change, or delete Contacts
    """
    def global_positioning_system(address):
        """
        Global Positioning System (GPS) Coordinates Finder
        Returns GeoLocation of clients' address
        """
        print(address) # This will print the Dictionary data structure ie. Key,Value pair.
        address_str = address["street_address"]
        print(address_str) # This will print the street adress value, which is a string.

        data = {
            'key': config['GEO_TOKEN'],
            'q': address_str,
            'format': 'json'
        }

        try:
            geo_response = rqs.get(csts.GEO_URL, params=data).json()
        except Exception as err:
            raise Exception("Something went wrong with the geocoding URL") from err

        lat, lon = utils.approx_coordinates(float(geo_response[0]['lat']), float(geo_response[0]['lon']))

        if not lat and not lon:
            logg.error("Unable to determine address")

        more_data = {
        'key': config['GEO_TOKEN'],
        'lat': lat,
        'lon': lon,
        'format': 'json'}

        try:
            rev_geo_response = rqs.get(csts.REVERSE_URL, params=more_data)
        except Exception as err:
            raise Exception("Something went wrong with the reverse geocoding URL") from err

        try:
            res = [f" The Client's Location is {rev_geo_response.json()['display_name']}"]
            return render(request, "result.html", {'res': res})
        except KeyError as err:
            # "I got a KeyError - reason '%s' " % str(err)
            message="Invalid Address Try Again \
            \n ie. The University of Texas at Austin, Austin, TX 78712"
            return render(request, "info.html", {'message': message})

    if request.method == 'POST':
        res = {}
        res['first'] = request.POST['fname']
        res['last'] = request.POST['lname']
        res['phone']= request.POST['phone']
        res['email']= request.POST['email']
        res['st_address'] = request.POST['st_address']
        curr_location = {'street_address': res['st_address']}

        if utils.address_validator(curr_location):
            contact_profile = Contact(first_name = res['first'], last_name= res['last'], phone = res['phone'], email= res['email'], address= res['st_address'])
            contact_profile.save()
            logg.info(f"User entered {res['first']} Address which is {res['st_address']}")
            return global_positioning_system(curr_location)
