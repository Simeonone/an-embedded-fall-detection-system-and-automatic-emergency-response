# Generated by Django 5.0.6 on 2024-05-16 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FallDetectionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('dsp_time', models.IntegerField()),
                ('classification_time', models.IntegerField()),
                ('anomaly_time', models.IntegerField()),
                ('predicted_activity', models.CharField(max_length=20)),
                ('stand_count', models.IntegerField()),
                ('uncertain_count', models.IntegerField()),
                ('fall_count', models.IntegerField()),
                ('other_count', models.IntegerField()),
            ],
        ),
    ]