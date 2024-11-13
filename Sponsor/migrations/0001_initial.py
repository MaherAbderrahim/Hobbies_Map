# Generated by Django 5.1.2 on 2024-11-13 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_sponsor', models.CharField(max_length=100)),
                ('description_sponsor', models.TextField()),
                ('prix_sponsor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('url_site', models.URLField()),
                ('url_photos', models.URLField()),
                ('rentabilite_par_user', models.FloatField()),
            ],
        ),
    ]
