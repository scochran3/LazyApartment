from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Apartment(models.Model):

	address = models.CharField(max_length=200, null=True, blank=True)
	area = models.IntegerField(null=True, blank=True)
	bedrooms = models.IntegerField(null=True, blank=True)
	bikeScore = models.IntegerField(null=True, blank=True)
	transitScore = models.IntegerField(null=True, blank=True)
	walkScore = models.IntegerField(null=True, blank=True)
	datetime = models.DateTimeField(default=timezone.now)
	distanceToNearestIntersection = models.DecimalField(max_digits=9, decimal_places=4, null=True, blank=True)
	hasImage = models.BooleanField(null=True, blank=True)
	hasMap = models.BooleanField(null=True, blank=True)
	name = models.CharField(max_length=200, null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	sideOfStreet = models.CharField(max_length=1, null=True, blank=True)
	url = models.CharField(max_length=200, null=True, blank=True)
	longitude = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
	latitude = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
	includesArea = models.BooleanField(null=True, blank=True)
	advertisesNoFee = models.BooleanField(null=True, blank=True)
	isRepost = models.BooleanField(null=True, blank=True)
	postalCode = models.CharField(max_length=20, null=True, blank=True)
	neighborhood = models.CharField(max_length=101, null=True, blank=True)
	borough = models.CharField(max_length=50, default='None')

	def save(self, *args, **kwargs):
		self.neighborhood_slugged = slugify(self.neighborhood)
		super(Apartment, self).save(*args, **kwargs)

	def __str__(self):
		return "{} - {}".format(self.neighborhood, self.name)

	class Meta:
		unique_together = ('name', 'address')
