# Generated by Django 4.2.4 on 2023-12-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reception", "0003_remove_schedule_users_schedule_doctor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="message",
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
