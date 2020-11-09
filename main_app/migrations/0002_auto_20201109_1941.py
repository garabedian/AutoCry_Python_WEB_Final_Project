# Generated by Django 3.1.3 on 2020-11-09 17:41

from django.db import migrations, models
import main_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='age',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='build_year',
            field=models.IntegerField(default=2020, validators=[main_app.validators.year_validator]),
        ),
        migrations.AddField(
            model_name='item',
            name='make',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='item',
            name='model',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('sedan', 'SEDAN'), ('hatchback', 'HATCHBACK'), ('ESTATE', 'ESTATE'), ('mpv', 'MPV'), ('suv', 'SUV'), ('unknown', 'Unknown')], default='unknown', max_length=9),
        ),
    ]
