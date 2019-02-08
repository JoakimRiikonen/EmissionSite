# EmissionSite
Site deployed on https://emissionsite.herokuapp.com/ (free model so the server is usually sleeping, first load takes a while)

A website made with Python/Django that lets the user search carbon dioxide emissions by location. API for the website made with Django Rest Framework. Reaktors 'preliminary assignment for summer jobs in Turku' https://www.reaktor.com/preliminary-assignment-for-summer-jobs-turku/

## Features
- Pulls the data from www.worldbank.org and displays it
- Has an json api that allows queries either per country or per year
  - All data: https://emissionsite.herokuapp.com/api
  - Country: https://emissionsite.herokuapp.com/api/country/country_name_here
  - Year: https://emissionsite.herokuapp.com/api/year/year_here

## Problems
The free postgre database on heroku isn't large enough for all data to be posted, so as a solution the script used to pull the data only pulls data from the top 20 most emmitting countries. This could be fixed by paying for a proper database, but I haven't got that kind of money.
