# Generated by Django 3.1.3 on 2021-01-06 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210106_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
