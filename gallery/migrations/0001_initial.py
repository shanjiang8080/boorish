# Generated by Django 5.0.6 on 2025-01-04 18:53

import django.core.validators
import gallery.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, validators=[gallery.models.validate_no_comma, gallery.models.validate_no_leading_trailing_spaces])),
                ('color', models.CharField(choices=[('R', 'Artist'), ('G', 'Character'), ('P', 'Copyright'), ('N', 'Description')], default='N', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('file', models.FileField(max_length=255, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'avif', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'gif', 'webp', 'apng', 'svg', 'mp4', 'webm'])])),
                ('is_video', models.BooleanField(default=False, editable=False)),
                ('is_animated', models.BooleanField(default=False, editable=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('votes', models.IntegerField(default=0)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tags', models.ManyToManyField(blank=True, related_name='images', related_query_name='image', to='gallery.tag')),
            ],
        ),
    ]
