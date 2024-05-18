# Generated by Django 5.0.6 on 2024-05-18 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0002_falldetectiondata_accel_x_falldetectiondata_accel_y_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='anomaly_time',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='classification_time',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='dsp_time',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='fall_count',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='other_count',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='stand_count',
        ),
        migrations.RemoveField(
            model_name='falldetectiondata',
            name='uncertain_count',
        ),
        migrations.AddField(
            model_name='falldetectiondata',
            name='sample_num',
            field=models.IntegerField(default=0),
        ),
    ]
