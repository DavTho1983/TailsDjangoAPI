# Generated by Django 2.1.8 on 2019-04-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Postcodes', '0002_auto_20190414_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcode',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='postcode',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
        ),
    ]