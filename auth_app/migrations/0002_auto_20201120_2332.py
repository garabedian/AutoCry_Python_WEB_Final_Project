# Generated by Django 3.1.3 on 2020-11-20 21:32

from django.db import migrations, models
import django.utils.timezone
import main_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birth_year',
            field=models.IntegerField(default=django.utils.timezone.now, validators=[main_app.validators.year_validator]),
            preserve_default=False,
        ),
    ]