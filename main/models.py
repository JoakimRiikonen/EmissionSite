from django.db import models

# Create your models here.
class EmissionInYear(models.Model):
    country_name = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    emission_amount = models.CharField(max_length=25, null=True)
    population = models.CharField(max_length=10, null=True)

    class Meta:
        unique_together = ('country_name', 'year')

    def __str__(self):
        if self.emission_amount is not None and self.population is not None:
            return self.country_name + ", " + self.year + ", pop: " + self.population +  ", emissions:" + self.emission_amount
        elif self.emission_amount is not None:
            return self.country_name + ", " + self.year + ", pop: No data" +  ", emissions:" + self.emission_amount
        elif self.population is not None:
            return self.country_name + ", " + self.year + ", pop: " + self.population +  ", emissions: No data"
        else:
            return self.country_name + ", " + self.year + ", pop: No data" + ", emissions: No data"
