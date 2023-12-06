# Generated by Django 3.2.22 on 2023-11-27 06:26

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('description', models.TextField(blank=True)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=200)),
                ('event_description', models.CharField(max_length=560)),
                ('available_to', models.CharField(max_length=9)),
                ('event_start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='event start time')),
                ('event_end_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='event end time')),
                ('event_lattitude', models.DecimalField(decimal_places=8, max_digits=20, verbose_name='lattitude')),
                ('event_longitude', models.DecimalField(decimal_places=8, max_digits=20, verbose_name='longitude')),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
    ]