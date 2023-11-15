# Generated by Django 4.2.6 on 2023-11-11 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkapp', '0013_lifeinsurance'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthInsurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_id', models.CharField(max_length=100, unique=True)),
                ('policy_holder_name', models.CharField(max_length=255)),
                ('proposer_dob', models.DateField()),
                ('proposer_pan', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('company_name', models.CharField(max_length=255)),
                ('plan', models.CharField(max_length=255)),
                ('frequency', models.CharField(max_length=50)),
                ('nominee_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
    ]
