# Generated by Django 4.1.7 on 2023-04-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0002_rename_attribute_attack_attribute_modifier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='lvl',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
