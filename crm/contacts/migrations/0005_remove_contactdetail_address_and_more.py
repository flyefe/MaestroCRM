# Generated by Django 5.1.2 on 2024-11-07 03:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0004_remove_contactdetail_traffic_source_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactdetail",
            name="address",
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="address_city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="address_country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="address_first_line",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="address_postal_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="address_second_line",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name="Address",
        ),
    ]