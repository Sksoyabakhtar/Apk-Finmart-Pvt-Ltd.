# Generated by Django 4.2.6 on 2023-11-13 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkapp', '0018_bonds'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investor_name', models.CharField(max_length=255)),
                ('pan_number', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('asp_name', models.CharField(max_length=255)),
                ('nominee_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
