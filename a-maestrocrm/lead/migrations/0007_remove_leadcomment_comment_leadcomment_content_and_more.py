# Generated by Django 5.0.7 on 2024-08-07 19:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lead", "0006_rename_comment_leadcomment_comment"),
        ("team", "0004_alter_team_plan"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leadcomment",
            name="comment",
        ),
        migrations.AddField(
            model_name="leadcomment",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="leadcomment",
            name="team",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leads_comment",
                to="team.team",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="leadcomment",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lead_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
