# Generated by Django 3.1.5 on 2021-01-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_mgt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationdetails',
            name='percentage',
            field=models.FloatField(default=0.0),
        ),
    ]
