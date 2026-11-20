from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cineva', '0003_remove_tmdb_provider_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerplugin',
            name='download_url',
            field=models.CharField(blank=True, help_text='Plantilla descarga, p.ej. https://…/{id}', max_length=500),
        ),
    ]
