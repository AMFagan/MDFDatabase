# Generated by Django 2.2.3 on 2019-07-22 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdf_db_app', '0003_auto_20190722_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='aims',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='module',
            name='comments',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='module',
            name='reading',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='module',
            name='syllabus',
            field=models.TextField(default=''),
        ),
    ]
