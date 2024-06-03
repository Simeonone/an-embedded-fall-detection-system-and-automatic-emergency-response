# Generated by Django 5.0.6 on 2024-05-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_delete_falldetection'),
    ]

    operations = [
        migrations.CreateModel(
            name='FallDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_num', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('predicted_activity', models.CharField(max_length=20)),
                ('accel_x', models.FloatField()),
                ('accel_y', models.FloatField()),
                ('accel_z', models.FloatField()),
            ],
        ),
    ]
