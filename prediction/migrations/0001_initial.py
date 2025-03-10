# Generated by Django 5.0.6 on 2025-02-03 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopDisasters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_number', models.IntegerField()),
                ('cityName', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('floodProne_areas', models.CharField(max_length=100)),
                ('recentDisasters', models.CharField(max_length=100)),
            ],
        ),
    ]
