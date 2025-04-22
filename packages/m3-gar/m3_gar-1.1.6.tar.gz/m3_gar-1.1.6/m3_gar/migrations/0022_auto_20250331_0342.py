from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m3_gar', '0021_remove_version_processed'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddrCacheResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Наименование')),
                ('page', models.CharField(max_length=10, verbose_name='Номер страницы')),
                ('data', models.TextField(verbose_name='Итоговые строки')),
            ],
            options={
                'verbose_name': 'Готовые результаты по запросу конкретного адреса',
                'verbose_name_plural': 'Готовые результаты по запросу конкретного адреса',
            },
        ),
        migrations.AddIndex(
            model_name='addrcacheresult',
            index=models.Index(fields=['name'], name='m3_gar_addr_name_ec91da_idx'),
        ),
    ]
