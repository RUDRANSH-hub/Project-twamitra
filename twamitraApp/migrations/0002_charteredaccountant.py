# Generated by Django 4.2.5 on 2023-12-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twamitraApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharteredAccountant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone', models.CharField(max_length=18)),
                ('alternatePhone', models.CharField(blank=True, max_length=18, null=True)),
                ('address', models.TextField(blank=True)),
            ],
        ),
    ]
