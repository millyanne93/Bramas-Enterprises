# Generated by Django 4.2.13 on 2024-05-31 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0003_rename_rental_days_booking_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
