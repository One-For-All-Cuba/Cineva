from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cineva", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tmdb_api_key", models.CharField(blank=True, max_length=128)),
                ("google_client_id", models.CharField(blank=True, max_length=255)),
                ("google_client_secret", models.CharField(blank=True, max_length=255)),
                ("qvapay_app_id", models.CharField(blank=True, max_length=128)),
                ("qvapay_app_secret", models.CharField(blank=True, max_length=255)),
                ("site_title", models.CharField(default="Cineva", max_length=120)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Configuración del sitio"},
        ),
        migrations.RemoveField(model_name="providerplugin", name="kind"),
        migrations.RemoveField(model_name="providerplugin", name="sort_order"),
        migrations.AddField(
            model_name="providerplugin",
            name="embed_url",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="providerplugin",
            name="priority",
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterModelOptions(
            name="providerplugin",
            options={"ordering": ["priority", "name"], "verbose_name": "Proveedor de video"},
        ),
    ]
