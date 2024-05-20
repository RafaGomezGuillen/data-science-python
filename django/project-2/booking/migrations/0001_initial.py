# Generated by Django 5.0.2 on 2024-02-24 10:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resource', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('status', models.CharField(choices=[('RE', 'Requested'), ('GR', 'Granted'), ('US', 'Used'), ('FI', 'Finantial')], default='RE', max_length=2)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resource.resource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
