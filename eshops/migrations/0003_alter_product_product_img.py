# Generated by Django 3.2.6 on 2021-09-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshops', '0002_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(blank=True, null=True, upload_to='product_img'),
        ),
    ]
