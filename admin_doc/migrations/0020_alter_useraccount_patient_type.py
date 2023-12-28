# Generated by Django 4.2.4 on 2023-12-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_doc", "0019_alter_useraccount_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="patient_type",
            field=models.CharField(
                blank=True,
                choices=[("N", "New Patient"), ("E", "Existing Patient")],
                max_length=1,
                null=True,
            ),
        ),
    ]