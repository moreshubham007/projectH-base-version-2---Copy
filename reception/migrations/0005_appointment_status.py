# Generated by Django 4.2.4 on 2023-12-08 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reception", "0004_appointment_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="status",
            field=models.BooleanField(default=False),
        ),
    ]
