# Generated by Django 2.1.7 on 2019-07-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_apartment_borough'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='delete',
            field=models.IntegerField(default=10),
        ),
    ]
