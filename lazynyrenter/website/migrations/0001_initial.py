# Generated by Django 2.1.7 on 2019-07-10 19:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('area', models.IntegerField(null=True)),
                ('bedrooms', models.IntegerField(null=True)),
                ('bikeScore', models.IntegerField(null=True)),
                ('transitScore', models.IntegerField(null=True)),
                ('walkScore', models.IntegerField(null=True)),
                ('datetime', models.DateField(default=django.utils.timezone.now)),
                ('distanceToNearestIntersection', models.DecimalField(decimal_places=4, max_digits=9, null=True)),
                ('has_image', models.BooleanField(null=True)),
                ('has_map', models.BooleanField(null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.IntegerField(null=True)),
                ('sideOfStreet', models.CharField(max_length=1, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('includes_area', models.BooleanField(null=True)),
                ('advertises_fee', models.BooleanField(null=True)),
                ('is_repost', models.BooleanField(null=True)),
                ('postalCode', models.CharField(max_length=20, null=True)),
                ('neighborhood', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
