from django.db import models
from django.contrib.auth.models import User
from PIL import Image

import json

# modelo dos personagens e criaturas


class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    background = models.CharField(max_length=20)
    lvl = models.IntegerField()
    job = models.CharField(max_length=20)
    race = models.CharField(max_length=20)
    experience = models.IntegerField(blank=True, null=True)
    portrait = models.ImageField(upload_to='portraits/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.portrait:
            img = Image.open(self.portrait.path)
            output_size = (150, 230)
            img.thumbnail(output_size)
            img.save(self.portrait.path)


# modelo das campanhas
class Campaign(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# modelo dos atributos dos personagens
class Atributes(models.Model):
    owner = models.ForeignKey("Character", on_delete=models.CASCADE)

    strength_modifier = models.IntegerField()
    strength_atribute = models.IntegerField()

    dexterity_modifier = models.IntegerField()
    dexterity_atribute = models.IntegerField()

    constituition_modifier = models.IntegerField()
    constituition_atribute = models.IntegerField()

    intelligence_modifier = models.IntegerField()
    intelligence_atribute = models.IntegerField()

    wisdom_modifier = models.IntegerField()
    wisdom_atribute = models.IntegerField()

    charisma_modifier = models.IntegerField()
    charisma_atribute = models.IntegerField()

    def __str__(self):
        return self.owner.name


# proeficiencias
class Skills(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE)

    inspiration = models.IntegerField(blank=True, null=True)
    proeficiency = models.IntegerField(blank=True, null=True)

    strength_proeficiency = models.BooleanField(null=True, blank=True)
    dexterity_proeficiency = models.BooleanField(null=True, blank=True)
    constituition_proeficiency = models.BooleanField(null=True, blank=True)
    intelligence_proeficiency = models.BooleanField(null=True, blank=True)
    wisdom_proeficiency = models.BooleanField(null=True, blank=True)
    charisma_proeficiency = models.BooleanField(null=True, blank=True)

    athletics_proeficiency = models.BooleanField(null=True, blank=True)
    stunt_proeficiency = models.BooleanField(null=True, blank=True)
    stealth_proeficiency = models.BooleanField(null=True, blank=True)
    sleight_proeficiency = models.BooleanField(null=True, blank=True)
    arcana_proeficiency = models.BooleanField(null=True, blank=True)
    history_proeficiency = models.BooleanField(null=True, blank=True)
    investigation_proeficiency = models.BooleanField(null=True, blank=True)
    medicine_proeficiency = models.BooleanField(null=True, blank=True)
    nature_proeficiency = models.BooleanField(null=True, blank=True)
    religion_proeficiency = models.BooleanField(null=True, blank=True)
    acting_proeficiency = models.BooleanField(null=True, blank=True)
    bluff_proeficiency = models.BooleanField(null=True, blank=True)
    intimidation_proeficiency = models.BooleanField(null=True, blank=True)
    intuition_proeficiency = models.BooleanField(null=True, blank=True)
    persuasion_proeficiency = models.BooleanField(null=True, blank=True)
    animal_proeficiency = models.BooleanField(null=True, blank=True)
    perception_proeficiency = models.BooleanField(null=True, blank=True)
    survive_proeficiency = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.owner.name


# caracteristicas
class Characteristics(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE)

    class_armor = models.IntegerField()
    iniciative = models.IntegerField()
    displacement = models.IntegerField()
    hp = models.IntegerField()

    language_and_other_skills = models.TextField(max_length=5000, null=True, blank=True)

    pc = models.IntegerField(null=True, blank=True)
    pp = models.IntegerField(null=True, blank=True)
    po = models.IntegerField(null=True, blank=True)
    pl = models.IntegerField(null=True, blank=True)
    da = models.IntegerField(null=True, blank=True)

    ideals = models.TextField(max_length=5000, null=True, blank=True)
    ligations = models.TextField(max_length=5000, null=True, blank=True)
    defects = models.TextField(max_length=5000, null=True, blank=True)

    characteristics_and_skills = models.TextField(max_length=5000, null=True, blank=True)

    appaerance = models.TextField(max_length=5000, null=True, blank=True)
    other_characteristics = models.TextField(max_length=5000, null=True, blank=True)
    allies_and_organizations = models.TextField(max_length=5000, null=True, blank=True)

    inventory = models.TextField(max_length=5000, null=True, blank=True)

    history = models.TextField(max_length=50000, null=True, blank=True)

    def __str__(self):
        return self.owner.name


# modelo dos ataques
class Attack(models.Model):
    owner = models.ForeignKey("Character", on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    magic_lvl = models.CharField(max_length=30, blank=True, null=True)

    dice_1 = models.CharField(max_length=500, null=True, blank=True)
    dice_2 = models.CharField(max_length=500, null=True, blank=True)
    dice_3 = models.CharField(max_length=500, null=True, blank=True)

    roll_1 = models.IntegerField(null=True, blank=True)
    roll_2 = models.IntegerField(null=True, blank=True)
    roll_3 = models.IntegerField(null=True, blank=True)

    damage_modifier = models.IntegerField(null=True, blank=True)
    attribute_modifier = models.TextField(max_length=12, null=True, blank=True)

    proficiency = models.BooleanField()
    description = models.TextField(max_length=5000, null=True, blank=True)

    type = models.CharField(max_length=8)

    def __str__(self):
        return self.name

# modelo das mensagens
class Message(models.Model):
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    owner = models.ForeignKey("Character", on_delete=models.CASCADE)

    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.owner.name
