# Generated by Django 4.1.7 on 2023-04-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0013_alter_attack_attribute_modifier_alter_attack_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attack',
            name='magic_lvl',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
