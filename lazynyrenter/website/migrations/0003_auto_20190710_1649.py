# Generated by Django 2.1.7 on 2019-07-10 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190710_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]