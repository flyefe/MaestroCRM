# Generated by Django 5.1.2 on 2024-10-30 18:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactdetail",
            old_name="contact_status",
            new_name="status",
        ),
    ]