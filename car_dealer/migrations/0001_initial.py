# Generated by Django 4.2.13 on 2024-05-28 22:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)])),
                ('city', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CarDealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_info', models.CharField(max_length=100)),
                ('wallet', models.IntegerField(default=0)),
                ('car_dealer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='car_dealer.location')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('capacity', models.CharField(max_length=2)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available', models.BooleanField(default=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='car_photos/')),
                ('description', models.CharField(max_length=100)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='car_dealer.location')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='car_dealer.cardealer')),
            ],
        ),
    ]