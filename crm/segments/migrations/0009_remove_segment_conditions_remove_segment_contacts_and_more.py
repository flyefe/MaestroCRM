# Generated by Django 5.1.2 on 2024-11-27 21:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("segments", "0008_remove_segment_created_at_remove_segment_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="segment",
            name="conditions",
        ),
        migrations.RemoveField(
            model_name="segment",
            name="contacts",
        ),
        migrations.RemoveField(
            model_name="segment",
            name="description",
        ),
        migrations.RemoveField(
            model_name="segment",
            name="type",
        ),
        migrations.RemoveField(
            model_name="segment",
            name="value",
        ),
    ]