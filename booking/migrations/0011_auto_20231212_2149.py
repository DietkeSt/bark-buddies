# Generated by Django 3.2.23 on 2023-12-12 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20231212_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='available_dates',
        ),
        migrations.DeleteModel(
            name='Date',
        ),
        migrations.AddField(
            model_name='dateavailability',
            name='available_time_slots',
            field=models.ManyToManyField(blank=True, to='booking.TimeSlot'),
        ),
    ]
