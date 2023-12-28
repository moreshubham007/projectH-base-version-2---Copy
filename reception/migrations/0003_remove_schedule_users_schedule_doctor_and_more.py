# Generated by Django 4.2.4 on 2023-12-08 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reception", "0002_schedule_available_time_from_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schedule",
            name="users",
        ),
        migrations.AddField(
            model_name="schedule",
            name="doctor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedules",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="daysoftheweek",
            name="available_days",
            field=models.CharField(
                choices=[
                    ("M", "Monday"),
                    ("T", "Tuesday"),
                    ("W", "Wednesday"),
                    ("H", "Thursday"),
                    ("F", "Friday"),
                    ("S", "Saturday"),
                    ("U", "Sunday"),
                ],
                max_length=1,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("appointment_id", models.CharField(max_length=4, null=True)),
                ("date", models.DateField(null=True)),
                ("time", models.TimeField(null=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_patients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]