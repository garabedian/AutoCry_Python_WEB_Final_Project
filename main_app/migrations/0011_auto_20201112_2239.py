# Generated by Django 3.1.3 on 2020-11-12 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20201112_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_url',
            field=models.URLField(blank=True, default='data:image/png;base64,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'),
        ),
    ]
