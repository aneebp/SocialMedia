# Generated by Django 5.0.2 on 2024-05-02 08:11

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_alter_profile_bio"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post_Upload",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("user", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="post")),
                ("caption", models.TextField()),
                ("no_of_like", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.AlterField(
            model_name="profile",
            name="profileImg",
            field=models.ImageField(
                default="images/blank-profile-piicture.png", upload_to="profile_images"
            ),
        ),
    ]
