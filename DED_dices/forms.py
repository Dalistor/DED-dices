from django import forms
from .models import *

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ['owner']
        fields = '__all__'

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        exclude = ['owner']
        fields = '__all__'

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['owner', 'team']
        fields = '__all__'

class AtributesForm(forms.ModelForm):
    class Meta:
        model = Atributes
        exclude = ['owner']
        fields = '__all__'

class SkillsForm(forms.ModelForm):
    #salvaguarda
    strength_proeficiency           = forms.BooleanField(required=False, initial=False)
    dexterity_proeficiency          = forms.BooleanField(required=False, initial=False)
    constituition_proeficiency      = forms.BooleanField(required=False, initial=False)
    intelligence_proeficiency       = forms.BooleanField(required=False, initial=False)
    wisdom_proeficiency             = forms.BooleanField(required=False, initial=False)
    charisma_proeficiency           = forms.BooleanField(required=False, initial=False)

    #habilidades
    athletics_proeficiency          = forms.BooleanField(required=False, initial=False)
    stunt_proeficiency              = forms.BooleanField(required=False, initial=False)
    stealth_proeficiency            = forms.BooleanField(required=False, initial=False)
    sleight_proeficiency            = forms.BooleanField(required=False, initial=False)
    arcana_proeficiency             = forms.BooleanField(required=False, initial=False)
    history_proeficiency            = forms.BooleanField(required=False, initial=False)
    investigation_proeficiency      = forms.BooleanField(required=False, initial=False)
    medicine_proeficiency           = forms.BooleanField(required=False, initial=False)
    nature_proeficiency             = forms.BooleanField(required=False, initial=False)
    religion_proeficiency           = forms.BooleanField(required=False, initial=False)
    acting_proeficiency             = forms.BooleanField(required=False, initial=False)
    bluff_proeficiency              = forms.BooleanField(required=False, initial=False)
    intimidation_proeficiency       = forms.BooleanField(required=False, initial=False)
    intuition_proeficiency          = forms.BooleanField(required=False, initial=False)
    persuasion_proeficiency         = forms.BooleanField(required=False, initial=False)
    animal_proeficiency             = forms.BooleanField(required=False, initial=False)
    perception_proeficiency         = forms.BooleanField(required=False, initial=False)
    survive_proeficiency            = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Skills
        exclude = ['owner']
        fields = '__all__'

class CharacteristicsForm(forms.ModelForm):
    class Meta:
        model = Characteristics
        exclude = ['owner']
        fields = '__all__'

class AttackForm(forms.ModelForm):
    class Meta:
        model = Attack
        exclude = ['owner']
        fields = '__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['owner', 'campaign']
        fields = '__all__'