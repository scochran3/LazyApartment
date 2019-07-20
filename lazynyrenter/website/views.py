from django.shortcuts import render
from .models import Apartment
from django.utils.text import slugify
from django_pandas.io import read_frame
from django.db.models import Count
import createAreaVisualizations



def index(request):
	context = {}

	return render(request, 'website/index.html', {})

def byNeighborhood(request):
	
	neighborhoods = Apartment.objects.order_by('neighborhood').values('neighborhood').distinct()

	context = {'neighborhoods': neighborhoods}

	return render(request, 'website/allNeighborhoods.html', context)


def byZipCode(request):

	zipCodes = Apartment.objects.values('postalCode').annotate(count=Count('postalCode')).order_by('-count')[0:100]

	context = {'zipCodes': zipCodes}
	
	return render(request, 'website/allZipCodes.html', context)


def byBorough(request):

	boroughs = Apartment.objects.order_by('borough').values('borough').distinct().exclude(borough="None")

	context = {'boroughs': boroughs}
	
	return render(request, 'website/allBoroughs.html', context)


def boroughData(request, borough):

	# Unslug neighborhood
	borough = unslugifyWord(borough)

	# Filter for these neighborhoods
	areaQuerySet = Apartment.objects.filter(borough=borough)
	allApartmentsQueryset = Apartment.objects.all()

	# Put data into a dataframe
	area_df = read_frame(areaQuerySet)
	all_apartments_df = read_frame(allApartmentsQueryset)

	# Figures
	priciestApartments = createAreaVisualizations.listOfApartments(area_df, 'priciest')
	cheapestApartments = createAreaVisualizations.listOfApartments(area_df, 'cheapest')
	priceOverTime = createAreaVisualizations.plotOverTime(area_df, all_apartments_df, 'borough', 'mean', compare=True)
	priceHistogram = createAreaVisualizations.priceHistogram(area_df, 15)
	squareFootageHistogram = createAreaVisualizations.squareFootageHistogram(area_df, 15)
	priceByBedrooms = createAreaVisualizations.averagePriceByBedrooms(area_df)
	areaVersusPrice = createAreaVisualizations.areaVersusPrice(area_df)
	areaPrices = createAreaVisualizations.areaPrices(all_apartments_df, borough, 'borough')
	areaByBedrooms = createAreaVisualizations.averageSizeByBedrooms(area_df)
	easeOfGettingAround = createAreaVisualizations.easeOfGettingAround(all_apartments_df, borough, "borough")

	context = {'borough': borough,
				'priciestApartments': priciestApartments,
				'cheapestApartments': cheapestApartments,
				'priceOverTime': priceOverTime,
				'priceHistogram': priceHistogram,
				'squareFootageHistogram': squareFootageHistogram,
				'priceByBedrooms': priceByBedrooms,
				'areaVersusPrice': areaVersusPrice,
				'areaPrices': areaPrices,
				'areaByBedrooms': areaByBedrooms,
				'easeOfGettingAround': easeOfGettingAround
				}

	return render(request, 'website/boroughData.html', context)


def zipCodeData(request, zipCode):

	# Filter for these neighborhoods
	areaQuerySet = Apartment.objects.filter(postalCode=zipCode)
	allApartmentsQueryset = Apartment.objects.all()

	# Put data into a dataframe
	area_df = read_frame(areaQuerySet)
	all_apartments_df = read_frame(allApartmentsQueryset)
	# area_df.to_csv('area.csv')

	# Figures
	priciestApartments = createAreaVisualizations.listOfApartments(area_df, 'priciest')
	cheapestApartments = createAreaVisualizations.listOfApartments(area_df, 'cheapest')
	priceOverTime = createAreaVisualizations.plotOverTime(area_df, all_apartments_df, 'postalCode', 'mean', compare=True)
	priceHistogram = createAreaVisualizations.priceHistogram(area_df, 15)
	squareFootageHistogram = createAreaVisualizations.squareFootageHistogram(area_df, 15)
	priceByBedrooms = createAreaVisualizations.averagePriceByBedrooms(area_df)
	areaVersusPrice = createAreaVisualizations.areaVersusPrice(area_df)
	areaPrices = createAreaVisualizations.areaPrices(all_apartments_df, zipCode, 'postalCode')
	areaByBedrooms = createAreaVisualizations.averageSizeByBedrooms(area_df)
	easeOfGettingAround = createAreaVisualizations.easeOfGettingAround(all_apartments_df, zipCode, "postalCode")

	context = {'zipCode': zipCode,
				'priciestApartments': priciestApartments,
				'cheapestApartments': cheapestApartments,
				'priceOverTime': priceOverTime,
				'priceHistogram': priceHistogram,
				'squareFootageHistogram': squareFootageHistogram,
				'priceByBedrooms': priceByBedrooms,
				'areaVersusPrice': areaVersusPrice,
				'areaPrices': areaPrices,
				'areaByBedrooms': areaByBedrooms,
				'easeOfGettingAround': easeOfGettingAround
				}

	return render(request, 'website/zipCodeData.html', context)



def neighborhoodData(request, neighborhood):

	# Unslug neighborhood
	neighborhood = unslugifyWord(neighborhood)


	# Filter for these neighborhoods
	neighborhoodQueryset = Apartment.objects.filter(neighborhood=neighborhood)
	allApartmentsQueryset = Apartment.objects.all()

	# Put data into a dataframe
	neighborhood_df = read_frame(neighborhoodQueryset)
	all_apartments_df = read_frame(allApartmentsQueryset)

	# Figures
	priciestApartments = createAreaVisualizations.listOfApartments(neighborhood_df, 'priciest')
	cheapestApartments = createAreaVisualizations.listOfApartments(neighborhood_df, 'cheapest')
	priceOverTime = createAreaVisualizations.plotOverTime(neighborhood_df, all_apartments_df, 'neighborhood', 'mean', compare=True)
	priceHistogram = createAreaVisualizations.priceHistogram(neighborhood_df, 15)
	squareFootageHistogram = createAreaVisualizations.squareFootageHistogram(neighborhood_df, 15)
	priceByBedrooms = createAreaVisualizations.averagePriceByBedrooms(neighborhood_df)
	areaVersusPrice = createAreaVisualizations.areaVersusPrice(neighborhood_df)
	areaPrices = createAreaVisualizations.areaPrices(all_apartments_df, neighborhood, 'neighborhood')
	areaByBedrooms = createAreaVisualizations.averageSizeByBedrooms(neighborhood_df)
	easeOfGettingAround = createAreaVisualizations.easeOfGettingAround(all_apartments_df, neighborhood, "neighborhood")

	# Return data to page
	context = {'neighborhood': neighborhood,
				'priciestApartments': priciestApartments,
				'cheapestApartments': cheapestApartments,
				'priceOverTime': priceOverTime,
				'priceHistogram': priceHistogram,
				'squareFootageHistogram': squareFootageHistogram,
				'priceByBedrooms': priceByBedrooms,
				'areaVersusPrice': areaVersusPrice,
				'areaPrices': areaPrices,
				'areaByBedrooms': areaByBedrooms,
				'easeOfGettingAround': easeOfGettingAround
				}

	return render(request, 'website/neighborhoodData.html', context)


def unslugifyWord(word):
	word = word.replace('-', ' ').title().replace('And', 'and')
	return word