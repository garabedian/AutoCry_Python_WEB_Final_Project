# Generated by Django 3.1.3 on 2020-11-24 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('sedan', 'SEDAN'), ('hatchback', 'HATCHBACK'), ('ESTATE', 'ESTATE'), ('mpv', 'MPV'), ('suv', 'SUV'), ('unknown', 'Unknown')], default='unknown', max_length=9)),
                ('make', models.CharField(default='', max_length=15)),
                ('model', models.CharField(default='', max_length=20)),
                ('build_year', models.IntegerField(validators=[main_app.validators.year_validator])),
                ('description', models.TextField()),
                ('image_type', models.CharField(choices=[('web_image', 'WEB Image'), ('local_image', 'Local or No Image')], max_length=11)),
                ('image_url', models.URLField(blank=True, default='https://s.clipartkey.com/mpngs/s/39-392476_transparent-jeep-clipart-audi-a4-2014-front.png')),
                ('image_file', models.ImageField(blank=True, default='/images/car.png', upload_to='images')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=200)),
                ('published', models.DateField()),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item')),
            ],
        ),
    ]
