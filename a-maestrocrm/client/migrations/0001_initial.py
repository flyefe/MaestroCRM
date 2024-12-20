# Generated by Django 5.0.7 on 2024-07-29 07:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(default="FirstName", max_length=255)),
                (
                    "middle_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("last_name", models.CharField(default="LastName", max_length=255)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "services",
                    models.CharField(
                        choices=[
                            ("POF", "POF"),
                            ("Insurance", "Insurance"),
                            ("Visa Processing", "Visa Processing"),
                            ("Admission processing", "Admission processing"),
                            ("Visa fee payment", "Visa fee payment"),
                        ],
                        default="Visa Processing",
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Open"), ("closed", "Closed")],
                        default="open",
                        max_length=50,
                    ),
                ),
                ("open_date", models.DateTimeField(blank=True, null=True)),
                ("close_date", models.DateTimeField(blank=True, null=True)),
                (
                    "traffic_source",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "converted_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_clients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "converted_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="converted_clients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
