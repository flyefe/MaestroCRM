# Generated by Django 5.1.2 on 2024-11-18 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0006_remove_contactdetail_address_city_and_more"),
        ("settings", "0004_tag"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactdetail",
            name="tags",
        ),
        migrations.AlterField(
            model_name="log",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_log",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="tags",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="contact", to="settings.tag"
            ),
        ),
    ]
