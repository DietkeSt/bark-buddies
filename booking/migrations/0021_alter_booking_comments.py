# Generated by Django 3.2.23 on 2024-01-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0020_auto_20240103_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='comments',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]
