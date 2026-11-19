# Generated manually for Cineva ProviderPlugin
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProviderPlugin",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=64, unique=True)),
                ("name", models.CharField(max_length=120)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("catalog", "Catálogo / metadata"),
                            ("auth", "Autenticación"),
                            ("payment", "Pagos"),
                            ("player", "Reproductor / video"),
                            ("other", "Otro"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("enabled", models.BooleanField(default=False)),
                ("config", models.JSONField(blank=True, default=dict)),
                ("sort_order", models.PositiveIntegerField(default=100)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
    ]
