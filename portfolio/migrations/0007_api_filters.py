# Generated by Django 4.2.7 on 2023-11-26 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_pagereview'),
    ]

    operations = [
        migrations.CreateModel(
            name='API_filters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(help_text='Select the time that interests you.', max_length=4, verbose_name='Time')),
                ('geo', models.CharField(help_text=' "BE": "Belgium",\n                    "BG": "Bulgaria",\n                    "CZ": "Czechia",\n                    "DK": "Denmark",\n                    "DE": "Germany",\n                    "EE": "Estonia",\n                    "IE": "Ireland",\n                    "EL": "Greece",\n                    "ES": "Spain",\n                    "FR": "France",\n                    "HR": "Croatia",\n                    "IT": "Italy",\n                    "CY": "Cyprus",\n                    "LV": "Latvia",\n                    "LT": "Lithuania",\n                    "LU": "Luxembourg",\n                    "HU": "Hungary",\n                    "MT": "Malta",\n                    "NL": "Netherlands",\n                    "AT": "Austria",\n                    "PL": "Poland",\n                    "PT": "Portugal",\n                    "RO": "Romania",\n                    "SI": "Slovenia",\n                    "SK": "Slovakia",\n                    "FI": "Finland",\n                    "SE": "Sweden",\n                    "IS": "Iceland",\n                    "NO": "Norway",\n                    "CH": "Switzerland" ', max_length=50, verbose_name='EU countries')),
                ('indic_he', models.CharField(help_text='"HLY_0": "Healthy life years in absolute value at birth",\n                    "LE_0": "Life expectancy in absolute value at birth",\n                    "HLY_50": "Healthy life years in absolute value at 50",\n                    "LE_50": "Life expectancy in absolute value at 50",\n                    "HLY_65": "Healthy life years in absolute value at 65",\n                    "LE_65": "Life expectancy in absolute value at 65" ', max_length=20, verbose_name='Report tipe')),
            ],
            options={
                'verbose_name': 'API_filters',
                'verbose_name_plural': 'API_filters',
            },
        ),
    ]
