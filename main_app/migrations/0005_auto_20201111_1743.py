# Generated by Django 3.1.3 on 2020-11-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_like_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_file',
            field=models.ImageField(default='', upload_to='images'),
        ),
        migrations.AddField(
            model_name='item',
            name='image_type',
            field=models.CharField(choices=[('web_image', 'WEB Image'), ('local_image', 'Local Image'), ('no_image', 'No Image')], default='no_image', max_length=11),
        ),
    ]
