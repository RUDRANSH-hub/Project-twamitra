# Generated by Django 4.2.5 on 2023-12-24 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twamitraApp', '0008_corporatedb_corporatepayments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporatedb',
            name='active_till',
            field=models.DateField(null=True),
        ),
    ]