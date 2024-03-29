from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_cleanup.signals import cleanup_pre_delete
from django.utils import timezone
from datetime import timedelta

from PIL import Image

# modelo dos personagens e criaturas


class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    background = models.CharField(max_length=20)
    lvl = models.IntegerField()
    job = models.CharField(max_length=20)
    race = models.CharField(max_length=20)
    experience = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(1000000000)])
    portrait = models.ImageField(upload_to='portraits/', null=True, blank=True)

    allocated_campaign = models.ForeignKey('Campaign', on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.portrait:
            img = Image.open(self.portrait.path)
            output_size = (150, 230)
            img.thumbnail(output_size)
            img.save(self.portrait.path)


class Entity(models.Model):
    owner = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    portrait = models.ImageField(upload_to='portraits/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

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
    team = models.ManyToManyField(User, related_name='team', blank=True)
    cover = models.ImageField(upload_to='campaign_cover/', null=True, blank=True)

    chat_private = models.BooleanField(default=False)

    history = models.TextField(max_length=99999999, null=True, blank=True)
    notes = models.TextField(max_length=99999999, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# modelo dos atributos dos personagens
class Atributes(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, null=True, blank=True)
    entity_owner = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)

    strength_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    strength_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    dexterity_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    dexterity_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    constituition_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    constituition_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    intelligence_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    intelligence_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    wisdom_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    wisdom_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    charisma_modifier = models.IntegerField(validators=[MaxValueValidator(20)])
    charisma_atribute = models.IntegerField(validators=[MaxValueValidator(50)])

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.owner:
            return self.owner.name
        else:
            return self.entity_owner.name
        


# proeficiencias
class Skills(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, null=True, blank=True)
    entity_owner = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)

    inspiration = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(100)])
    proeficiency = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(20)])

    strength_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    dexterity_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    constituition_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    intelligence_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    wisdom_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    charisma_proeficiency = models.IntegerField(null=True, blank=True, default=0)

    athletics_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    stunt_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    stealth_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    sleight_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    arcana_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    history_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    investigation_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    medicine_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    nature_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    religion_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    acting_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    bluff_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    intimidation_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    intuition_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    persuasion_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    animal_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    perception_proeficiency = models.IntegerField(null=True, blank=True, default=0)
    survive_proeficiency = models.IntegerField(null=True, blank=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.owner:
            return self.owner.name
        else:
            return self.entity_owner.name


# caracteristicas
class Characteristics(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, null=True, blank=True)
    entity_owner = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)

    class_armor = models.IntegerField(validators=[MaxValueValidator(100)])
    iniciative = models.IntegerField(validators=[MaxValueValidator(20)])
    displacement = models.IntegerField(validators=[MaxValueValidator(1000)])
    hp_max = models.IntegerField(validators=[MaxValueValidator(10000)])
    hp = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)])

    class_armor_temp = models.IntegerField(null=True, blank=True)
    displacement_temp = models.IntegerField(null=True, blank=True)
    hp_temp = models.IntegerField(null=True, blank=True)

    language_and_other_skills = models.TextField(max_length=5000, null=True, blank=True)

    pc = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])
    pp = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])
    po = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])
    pl = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])
    da = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(1000)])

    ideals = models.TextField(max_length=5000, null=True, blank=True)
    ligations = models.TextField(max_length=5000, null=True, blank=True)
    defects = models.TextField(max_length=5000, null=True, blank=True)

    characteristics_and_skills = models.TextField(max_length=5000, null=True, blank=True)

    appaerance = models.TextField(max_length=5000, null=True, blank=True)
    other_characteristics = models.TextField(max_length=5000, null=True, blank=True)
    allies_and_organizations = models.TextField(max_length=5000, null=True, blank=True)

    equipments = models.TextField(max_length=2000, null=True, blank=True)

    inventory = models.TextField(max_length=5000, null=True, blank=True)

    history = models.TextField(max_length=50000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.owner:
            return self.owner.name
        else:
            return self.entity_owner.name


# modelo dos ataques
class Attack(models.Model):
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, null=True, blank=True)
    entity_owner = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=30)

    magic_lvl = models.CharField(max_length=30, blank=True, null=True)

    dice_1 = models.CharField(max_length=10, default='Nenhum', blank=True)
    dice_2 = models.CharField(max_length=10, default='Nenhum', blank=True)
    dice_3 = models.CharField(max_length=10, default='Nenhum', blank=True)

    roll_1 = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    roll_2 = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    roll_3 = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])

    damage_modifier = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    attribute_modifier = models.TextField(max_length=12, default='Nenhum', blank=True)

    proficiency = models.BooleanField()
    description = models.TextField(max_length=5000, null=True, blank=True)

    type = models.CharField(max_length=8)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.owner:
            return self.owner.name
        else:
            return self.entity_owner.name

# modelo das mensagens
class Message(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, null=True, blank=True)
    entity_owner = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)

    username = models.CharField(max_length=50, null=True, blank=True)

    content = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.owner:
            return self.owner.name
        elif self.entity_owner:
            return self.entity_owner.name
        else:
            return 'Mestre'


#funções do banco de dados

@receiver(post_save, sender=Message)
def schedule_exclusion(sender, instance, **kwargs):
    now = timezone.now()
    day_after = now + timedelta(days=1)
    cleanup_pre_delete.send(sender=instance.__class__, instance=instance, when=day_after)