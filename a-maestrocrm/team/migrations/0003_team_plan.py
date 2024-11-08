# Generated by Django 5.0.7 on 2024-08-01 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0002_plan_team_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team",
                to="team.plan",
            ),
            preserve_default=False,
        ),
    ]
