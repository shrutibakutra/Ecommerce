# Generated by Django 3.1.3 on 2021-01-06 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(upload_to='media'),
        ),
    ]
