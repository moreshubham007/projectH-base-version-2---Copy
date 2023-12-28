# Generated by Django 4.2.4 on 2023-12-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_doc", "0017_alter_useraccount_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="patient_type",
            field=models.CharField(
                choices=[("N", "New Patient"), ("E", "Existing Patient")],
                max_length=1,
                null=True,
            ),
        ),
    ]