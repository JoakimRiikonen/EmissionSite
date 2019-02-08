from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import generics
from .serializers import EIYserializer
from main.models import EmissionInYear

# Create your views here.
def homepage(request):

    # adds spaces to the population number, making it look nicer
    # e.g: 12345678 -> 12 345 678
    def addSpaceToPop(population):
        length = len(population)
        alist = list(population)
        for i in range(length-3, -1, -3):
            alist.insert(i, " ")
        return ''.join(alist)

    # get list of country names, used in dropdown select
    countries = []
    for i in EmissionInYear.objects.all().filter(year="2000"):
        countries.append(i.country_name)
    countries.sort()

    # default values
    country_name = "none"
    percapita = False
    countryemissions = []

    # When user searches for a country
    if request.method == "POST":
        country_name = request.POST['country_name']
        percapita = 'percapita' in request.POST

        EIY_list = EmissionInYear.objects.all() \
                        .filter(country_name=country_name)

        # if percapita was checked
        if percapita:
            for o in EIY_list:
                dict = {}
                dict['year'] = o.year
                dict['emissions'] = "No data" if o.emission_amount is None \
                                    or o.population is None \
                                    else float(o.emission_amount) / int(o.population)
                dict['population'] = "No data" if o.population is None \
                                    else addSpaceToPop(o.population)
                countryemissions.append(dict)
        # else
        else:
            for o in EIY_list:
                dict = {}
                dict['year'] = o.year
                dict['emissions'] = "No data" if o.emission_amount is None \
                                    else o.emission_amount
                dict['population'] = "No data" if o.population is None \
                                    else addSpaceToPop(o.population)
                countryemissions.append(dict)

    return render(request=request,
                template_name="main/home.html",
                context={"countries":countries, "country_name":country_name,
                "percapita":percapita, "table":countryemissions}
                )


# Get all data
class AllView(generics.ListAPIView):
    queryset = EmissionInYear.objects.all()
    serializer_class = EIYserializer


# Get data by country
class CountryView(generics.ListAPIView):
    serializer_class = EIYserializer

    def get_queryset(self):
        country = self.kwargs['country']
        return EmissionInYear.objects.filter(country_name=country)


# Get data by year
class YearView(generics.ListAPIView):
    serializer_class = EIYserializer

    def get_queryset(self):
        year = self.kwargs['year']
        return EmissionInYear.objects.filter(year=year)
