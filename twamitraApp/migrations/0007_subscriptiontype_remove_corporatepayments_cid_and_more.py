# Generated by Django 4.2.5 on 2023-12-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twamitraApp', '0006_corporatedb_created_at_corporatedb_has_paid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('value', models.PositiveIntegerField()),
                ('default_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='corporatepayments',
            name='cid',
        ),
        migrations.DeleteModel(
            name='CorporateDB',
        ),
        migrations.DeleteModel(
            name='CorporatePayments',
        ),
    ]