# Generated by Django 3.0 on 2020-07-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheques', '0002_auto_20200623_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]