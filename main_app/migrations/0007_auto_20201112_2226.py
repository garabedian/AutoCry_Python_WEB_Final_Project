# Generated by Django 3.1.3 on 2020-11-12 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20201111_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_file',
            field=models.ImageField(blank=True, default='/images/car.png', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_type',
            field=models.CharField(choices=[('web_image', 'WEB Image'), ('local_image', 'Local Image'), ('no_image', 'No Image')], max_length=11),
        ),
    ]