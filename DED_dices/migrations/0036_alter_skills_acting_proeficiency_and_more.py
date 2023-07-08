# Generated by Django 4.1.7 on 2023-06-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DED_dices', '0035_campaign_history_campaign_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='acting_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='animal_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='arcana_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='athletics_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='bluff_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='charisma_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='constituition_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='dexterity_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='history_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='intelligence_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='intimidation_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='intuition_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='investigation_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='medicine_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='nature_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='perception_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='persuasion_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='religion_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='sleight_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='stealth_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='strength_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='stunt_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='survive_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='wisdom_proeficiency',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]