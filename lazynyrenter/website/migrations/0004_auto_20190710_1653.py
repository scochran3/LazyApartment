# Generated by Django 2.1.7 on 2019-07-10 20:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20190710_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
