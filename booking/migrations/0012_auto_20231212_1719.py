# Generated by Django 3.2.23 on 2023-12-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20231211_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='times',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time_slots',
        ),
        migrations.AddField(
            model_name='booking',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='time_slot',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Noon', 'Noon'), ('Evening', 'Evening')], default='Morning', max_length=10),
        ),
        migrations.DeleteModel(
            name='Time',
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
    ]