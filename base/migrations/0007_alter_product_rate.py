# Generated by Django 4.2.13 on 2024-05-21 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=1, max_digits=5),
        ),
    ]
