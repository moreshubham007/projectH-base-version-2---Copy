# Generated by Django 4.2.4 on 2023-11-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_doc", "0005_alter_useraccount_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="user_id",
            field=models.CharField(max_length=10),
        ),
    ]