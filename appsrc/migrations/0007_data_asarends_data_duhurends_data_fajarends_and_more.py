# Generated by Django 4.1.2 on 2023-06-25 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsrc', '0006_data_user_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='asarEnds',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='duhurEnds',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='fajarEnds',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='ishaEnds',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='maghribEnds',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
