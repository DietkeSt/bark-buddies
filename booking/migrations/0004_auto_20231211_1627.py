# Generated by Django 3.2.23 on 2023-12-11 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_booking_time_slot'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='booking',
            name='time_slots',
            field=models.ManyToManyField(to='booking.TimeSlot'),
        ),
    ]