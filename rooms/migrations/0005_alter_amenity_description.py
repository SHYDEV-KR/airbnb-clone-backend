# Generated by Django 4.1.1 on 2022-09-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_amenity_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
