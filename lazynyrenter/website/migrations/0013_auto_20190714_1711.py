# Generated by Django 2.1.7 on 2019-07-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20190710_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=101, null=True),
        ),
    ]