# Generated by Django 5.0.6 on 2024-05-20 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0012_image_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.FileField(editable=False, null=True, upload_to=''),
        ),
    ]
