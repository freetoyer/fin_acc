# Generated by Django 3.0 on 2020-06-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='inn',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
