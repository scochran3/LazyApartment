# Generated by Django 2.1.7 on 2019-07-21 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_apartment_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='delete',
        ),
    ]