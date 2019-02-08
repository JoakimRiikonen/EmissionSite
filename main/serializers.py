from rest_framework import serializers
from .models import EmissionInYear

class EIYserializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionInYear
        fields = ("country_name", "year", "emission_amount", "population")
