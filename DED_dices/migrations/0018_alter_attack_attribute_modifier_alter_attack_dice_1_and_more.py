# Generated by Django 4.1.7 on 2023-05-18 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0017_characteristics_hp_max_alter_characteristics_hp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attack',
            name='attribute_modifier',
            field=models.TextField(blank=True, default='Nenhum', max_length=12),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_1',
            field=models.CharField(blank=True, default='Nenhum', max_length=500),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_2',
            field=models.CharField(blank=True, default='Nenhum', max_length=500),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_3',
            field=models.CharField(blank=True, default='Nenhum', max_length=500),
        ),
    ]
