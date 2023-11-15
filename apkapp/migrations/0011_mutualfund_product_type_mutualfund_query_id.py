# Generated by Django 4.2.6 on 2023-11-11 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkapp', '0010_mutualfund'),
    ]

    operations = [
        migrations.AddField(
            model_name='mutualfund',
            name='product_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='mutualfund',
            name='query_id',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]