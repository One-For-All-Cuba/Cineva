from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cineva", "0002_siteconfig_provider_video"),
    ]

    operations = [
        migrations.RemoveField(model_name="siteconfig", name="tmdb_api_key"),
        migrations.AddField(
            model_name="providerplugin",
            name="catalog_url",
            field=models.CharField(blank=True, help_text="URL HTTPS de tu API de catálogo (JSON).", max_length=500),
        ),
        migrations.AddField(
            model_name="providerplugin",
            name="trailer_url",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
