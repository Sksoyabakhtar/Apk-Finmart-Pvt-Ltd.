# Generated by Django 4.2.6 on 2023-11-11 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkapp', '0014_healthinsurance'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_id', models.CharField(max_length=100, unique=True)),
                ('investor_name', models.CharField(max_length=255, verbose_name='Investor Name')),
                ('pan_number', models.CharField(max_length=10, verbose_name='PAN Number')),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('mobile', models.CharField(max_length=15, verbose_name='Mobile')),
                ('category', models.CharField(max_length=255, verbose_name='Category')),
                ('company_name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('frequency', models.CharField(max_length=255, verbose_name='Frequency')),
                ('nominee', models.CharField(max_length=255, verbose_name='Nominee')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
            ],
        ),
    ]
