# Generated by Django 4.2.4 on 2023-12-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_doc", "0016_useraccount_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="address",
            field=models.TextField(blank=True),
        ),
    ]
