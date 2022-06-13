'''Create your views here.'''
from pathlib import Path
import logging as logg
from django.shortcuts import render
import requests as rqs
from dotenv import dotenv_values
from . forms import LoginForm, AddressForm
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
    form = LoginForm(request.POST)
    if form.is_valid():
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username == 'my' and password == 'info':
                logg.info("Authenticated user")
                msg = 'Nice! Username and password was correct'
                return render(request, "info.html", {'message':msg})
        except:
            pass
    else:
        form = LoginForm()
        logg.info("Not Authenticated user")
        # count number of login attempts, block user from login
        msg = 'You will get blocked after 5 wrong attempts'
        return render(request, "login.html", {'message':msg, 'form':form})

def saved(request):
    '''This view will Display all saved contacts'''
    all_contacts = Contact.objects.all()
    return render(request,"saved.html", {"action":"Display all Contacts", "all_contacts":all_contacts})

def info(request):
    """
    Saves Clients/Users to Admin Site Contact book
    Admin will be able to add, change, or delete Contacts
    """
    def global_positioning_system(user_address):
        """
        Global Positioning System (GPS) Coordinates Finder
        Returns GeoLocation of clients' address
        """

        data = {
            'key': config['GEO_TOKEN'],
            'q': user_address,
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

    if request.POST:
        form = AddressForm(request.POST)
        res = {}
        res['first'] = request.POST['fname']
        res['last'] = request.POST['lname']
        res['phone']= request.POST['phone']
        res['email']= request.POST['email']
        if form.is_valid():
            try:
                name = form.cleaned_data.get('address')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                curr_loc = {
                    'name': name,
                    'city': city,
                    'state': state,
                    'country': country,
                    'zip_code': zip_code
                    }
            except:
                logg.info(f"Form is not valid")
                pass

        if utils.address_validator(curr_loc):
            print(curr_loc) # This will print the Dictionary data structure ie. Key,Value pair.
            location = " ".join([str(i) for i in curr_loc.values()])
            print(location) # This will print a string of the street address values.
            contact_profile = Contact(first_name = res['first'], last_name= res['last'], phone = res['phone'], email= res['email'], address= location)
            contact_profile.save()
            logg.info(f"User {res['first']} entered {res} and their Address is {location}")
            return global_positioning_system(location)
