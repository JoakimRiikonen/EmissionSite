# Generated by Django 2.1.5 on 2019-02-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190201_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissioninyear',
            name='population',
            field=models.CharField(max_length=10, null=True),
        ),
    ]