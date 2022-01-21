# Generated by Django 3.2.5 on 2021-07-23 15:23

from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import F


def copy_rpc_fields(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    chain_model = apps.get_model("chains", "chain")
    db_alias = schema_editor.connection.alias
    chain_model.objects.using(db_alias).all().update(
        safe_apps_rpc_uri=F("rpc_uri"),
        safe_apps_rpc_authentication=F("rpc_authentication"),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("chains", "0018_chain_rpc_authentication"),
    ]

    operations = [
        migrations.AddField(
            model_name="chain",
            name="safe_apps_rpc_authentication",
            field=models.CharField(
                choices=[
                    ("API_KEY_PATH", "Api Key Path"),
                    ("NO_AUTHENTICATION", "No Authentication"),
                ],
                default="NO_AUTHENTICATION",
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chain",
            name="safe_apps_rpc_uri",
            field=models.URLField(
                default="",
            ),
        ),
        migrations.RunPython(copy_rpc_fields, lambda apps, schema_editor: None),
    ]
