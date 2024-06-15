# Generated by Django 5.0.6 on 2024-05-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_color',
        ),
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('R', 'Artist'), ('G', 'Character'), ('P', 'Copyright'), ('N', 'Description')], default='N', max_length=1),
        ),
    ]
