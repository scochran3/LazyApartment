# Generated by Django 2.1.7 on 2019-07-11 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20190710_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='area',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='bedrooms',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='bikeScore',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='transitScore',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='walkScore',
            field=models.IntegerField(null=True),
        ),
    ]
