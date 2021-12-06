# Generated by Django 3.2 on 2021-04-29 08:22

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Provider",
            fields=[
                ("url", models.URLField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="SafeApp",
            fields=[
                ("url", models.URLField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("icon_url", models.URLField()),
                ("description", models.CharField(max_length=200)),
                (
                    "networks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="safe_apps.provider",
                    ),
                ),
            ],
        ),
    ]
