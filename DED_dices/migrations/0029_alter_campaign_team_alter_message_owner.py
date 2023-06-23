# Generated by Django 4.1.7 on 2023-06-17 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DED_dices', '0028_rename_alocated_campaign_character_allocated_campaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='team',
            field=models.ManyToManyField(blank=True, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DED_dices.character'),
        ),
    ]