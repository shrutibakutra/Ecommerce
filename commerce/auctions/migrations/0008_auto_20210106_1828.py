# Generated by Django 3.1.3 on 2021-01-06 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auctionlisting_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
