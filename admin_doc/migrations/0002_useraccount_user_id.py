# Generated by Django 4.2.4 on 2023-11-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_doc", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="user_id",
            field=models.CharField(default="001", max_length=7),
        ),
    ]
