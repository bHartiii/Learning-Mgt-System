# Generated by Django 3.1.5 on 2021-02-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210130_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='upated_by',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
