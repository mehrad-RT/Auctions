# Generated by Django 4.1.5 on 2023-09-01 10:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlistUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
