# Generated by Django 2.2 on 2019-04-13 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_ground', '0003_auto_20190412_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
