# Generated by Django 4.1.7 on 2023-04-24 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0006_alter_characteristics_da_alter_characteristics_pc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attack',
            name='damage_modifier',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='dice_3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='attack',
            name='rool_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='rool_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='rool_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attack',
            name='type',
            field=models.CharField(choices=[('Physical', 'Físico'), ('Magic', 'Mágico')], max_length=8),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='character',
            name='background',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='character',
            name='job',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='character',
            name='race',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='allies_and_organizations',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='appaerance',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='characteristics_and_skills',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='defects',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='history',
            field=models.TextField(blank=True, max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='ideals',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='inventory',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='language_and_other_skills',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='ligations',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='characteristics',
            name='other_characteristics',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
