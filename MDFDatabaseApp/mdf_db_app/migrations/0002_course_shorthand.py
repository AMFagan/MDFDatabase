# Generated by Django 2.2.5 on 2019-09-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdf_db_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='shorthand',
            field=models.CharField(default='', max_length=5),
        ),
    ]
