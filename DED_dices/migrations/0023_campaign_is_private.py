# Generated by Django 4.1.7 on 2023-06-10 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0022_campaign_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]