# Generated by Django 4.2.13 on 2024-05-21 20:01

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_product_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.generate_new_filename),
        ),
    ]
