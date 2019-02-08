import requests
import zipfile
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
from django.db import transaction

import os
# set the settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EmissionSite.settings")
# get the application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from main.models import EmissionInYear

#-----------------------------
# ONLY PULLS DATA FROM TOP20 EMITTING COUNTRIES
#
# This script pulls the population and co2 emissions data from
# http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml and
# http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml
# respectively and adds it to the sqlite3 database
#-----------------------------

#-----FETCH DATA FROM API-----
emissions_response = requests.get("http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml")
print("Emission data response:" + str(emissions_response.status_code))
population_response = requests.get("http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml")
print("Population data response:" + str(population_response.status_code))

# exit if data cannot be retrieved
if emissions_response.status_code != 200 or population_response.status_code != 200:
    exit()

#-----UNPACK EMISSION DATA-----
# get the zip of the data, save as BytesIO, then zip
emissions_zipfile = zipfile.ZipFile(BytesIO(emissions_response.content))
emissions_filename = ""
# the data filename has a seemingly random set of numbers at the end
# so the name has to be fetched like this
for name in emissions_zipfile.namelist():
    # The data filename starts with 'A', the other files are just metadata
    if name[0] == 'A':
        emissions_filename = name
        break
# XML as string
emissions_string = emissions_zipfile.open(emissions_filename).read().decode("utf-8")

emissions_root = ET.fromstring(emissions_string)

#-----UNPACK POPULATION DATA-----
# get the zip of the data, save as BytesIO, then zip
population_zipfile = zipfile.ZipFile(BytesIO(population_response.content))
population_filename = ""
# the data filename has a seemingly random set of numbers at the end
# so the name has to be fetched like this
for name in population_zipfile.namelist():
    # The data filename starts with 'A', the other files are just metadata
    if name[0] == 'A':
        population_filename = name
        break
# XML as string
population_string = population_zipfile.open(population_filename).read().decode("utf-8")

population_root = ET.fromstring(population_string)

# list of countries to pull from
countries = ["China", "United States", "India", "Russia", "Japan", "Germany",
            "Korea", "Iran", "Canada", "Saudi Arabia", "Brazil", "Mexico",
            "Indonesia", "South Africa", "United Kingdom", "Australia",
            "Italy", "Turkey", "France", "Poland"]

country_keys = ["CHN","USA","IND","RUS","JPN","DEU","KOR","IRN","CAN","SAU",
                "BRA","MEX","IDN","ZAF","GBR","AUS","ITA","TUR","FRA","POL"]

#-----WRITE TO DATABASE-----
# root[0] is the data label, which has all the records
with transaction.atomic():
    # delete the old database since its going to be replaced
    EmissionInYear.objects.all().delete()
    for echild, pchild in zip(emissions_root[0], population_root[0]):
        # child[0] is the country
        country = echild[0].text
        if country in countries:
            # year is child[2]
            year = echild[2].text
            # value is echild[3], can be None
            value = echild[3].text
            # population is pchild[3], can be None
            population = pchild[3].text

            # print the data of the current country
            print("Country:" + country + ", year:" + year)
            if echild[3].text is None:
                print("Emissions: No data")
            else:
                print("Emissions:" + value)
            if pchild[3].text is None:
                print("Pop: No data")
            else:
                print("Pop:" + population)
            print("----------")

            # save in database
            entry = EmissionInYear(country_name=country, year=year, emission_amount=value, population=population)
            entry.save()

print("Done!")
