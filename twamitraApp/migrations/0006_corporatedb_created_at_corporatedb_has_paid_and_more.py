# Generated by Django 4.2.5 on 2023-12-17 11:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('twamitraApp', '0005_alter_corporatedb_referralcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporatedb',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corporatedb',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='corporatedb',
            name='razorpay_order_id',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='generatedcode',
            name='percentage',
            field=models.CharField(choices=[('25', '25'), ('50', '50'), ('75', '75'), ('100', '100')], default='25%', max_length=20),
        ),
        migrations.CreateModel(
            name='CorporatePayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(max_length=255)),
                ('razorpay_payment_id', models.CharField(max_length=255)),
                ('razorpay_signature', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twamitraApp.corporatedb')),
            ],
        ),
    ]
