# Generated by Django 5.1.2 on 2024-11-07 19:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='u_event',
            field=models.ManyToManyField(related_name='eve', through='Event.User_Event', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='user_event',
            unique_together={('utilisateur', 'event')},
        ),
    ]