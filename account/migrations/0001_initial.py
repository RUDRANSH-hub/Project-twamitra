# Generated by Django 4.2.5 on 2023-10-10 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=254)),
            ],
        ),
    ]
