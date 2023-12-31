# Generated by Django 4.2.6 on 2023-11-13 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkapp', '0025_bonds_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixeddeposit',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='generalinsurance',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='healthinsurance',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='lifeinsurance',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='mutualfund',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
