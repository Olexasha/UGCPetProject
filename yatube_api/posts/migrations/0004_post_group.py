# Generated by Django 3.2.16 on 2024-07-03 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0003_auto_20240703_0113"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="posts.group",
            ),
        ),
    ]
