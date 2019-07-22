from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Apartment(models.Model):

	address = models.CharField(max_length=200, null=True, blank=True)
	area = models.IntegerField(null=True, blank=True)
	bedrooms = models.IntegerField(null=True, blank=True)
	bike_score = models.IntegerField(null=True, blank=True)
	transit_score = models.IntegerField(null=True, blank=True)
	walk_score = models.IntegerField(null=True, blank=True)
	datetime = models.DateTimeField(default=timezone.now)
	distance_to_nearest_intersection = models.DecimalField(max_digits=9, decimal_places=4, null=True, blank=True)
	has_image = models.BooleanField(null=True, blank=True)
	has_map = models.BooleanField(null=True, blank=True)
	name = models.CharField(max_length=200, null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	side_of_street = models.CharField(max_length=1, null=True, blank=True)
	url = models.CharField(max_length=200, null=True, blank=True)
	longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
	latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
	includes_area = models.BooleanField(null=True, blank=True)
	advertises_no_fee = models.BooleanField(null=True, blank=True)
	is_repost = models.BooleanField(null=True, blank=True)
	postal_code = models.CharField(max_length=20, null=True, blank=True)
	neighborhood = models.CharField(max_length=101, null=True, blank=True)
	borough = models.CharField(max_length=50, default='None')

	def save(self, *args, **kwargs):
		self.neighborhood_slugged = slugify(self.neighborhood)
		super(Apartment, self).save(*args, **kwargs)

	def __str__(self):
		return "{} - {}".format(self.neighborhood, self.name)

	class Meta:
		unique_together = ('name', 'address')
