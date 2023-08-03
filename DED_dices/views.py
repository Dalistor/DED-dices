from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.cache import never_cache

from .models import *
from .forms import *
from .functions import *
from .hash import *

import json

# redirecionar para uma view
@never_cache
def redirect_view(request):
    if request.user.is_authenticated:
        return redirect('/selection/')
    else:
        return redirect('/login/')


# login
@never_cache
def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('/selection/')

        else:
            error_message = 'Nome ou senha incorretos'

    return render(request, 'login.html', {
        'error_message': error_message
    })


# registro
@never_cache
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        verify = userVerify(username, email, password, password_confirm)
        if verify['is_valid']:
            new_user = User.objects.create_user(
                username=username, email=email, password=password)
            new_user.save()

            return redirect('/selection/')

        else:
            return render(request, 'register.html', {
                'error_message': verify['error_message']
            })

    else:
        return render(request, 'register.html')


# logout
@never_cache
def logout_view(request):
    logout(request)
    return redirect('/login/')


# seleção de conta
@never_cache
def selection_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        return render(request, 'selection.html')


# seleção de personagens
@never_cache
def player_selection_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    #pesquisa
    if request.GET.get('search'):
        search_input = request.GET['search_input']
        all_characters = Character.objects.filter(
            owner=request.user.id,
            name__icontains=search_input
        )

    else:
        all_characters = Character.objects.filter(owner=request.user.id)

    # trocar id por hash
    for character in all_characters:
        character.id = hash_id(character.id)

    return render(request, 'character_selection.html', {
        'all_characters': all_characters
    })


# deleção de personagem
def delete_character(request, hash):
    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')
    

    character = Character.objects.get(id=id)

    if character.owner == request.user:
        character.delete()
    else:
        return HttpResponse('Permissão não concedida')

    return redirect('/player_selection/')


# autosave do personagem
@csrf_exempt
def character_autosave(request, hash, field):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    character = Character.objects.get(id=id)

    if character.owner != request.user.id:
        return HttpResponse('Permissão não concedida')
    
    table = Characteristics.objects.get(owner=character.id)
    skill = Skills.objects.get(owner=character.id)

    if request.method == 'POST':
        if field == 'inspiration':
            skill.inspiration = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'class_armor_temp':
            table.class_armor_temp = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'displacement_temp':
            table.displacement_temp = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'hp_temp':
            table.hp_temp = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'pc':
            table.pc = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'pp':
            table.pp = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'po':
            table.po = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'pl':
            table.pl = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'da':
            table.da = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'equipments':
            table.equipments = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'inventory':
            table.inventory = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'history':
            table.history = request.POST['value'] if request.POST['value'] != '' else None

        elif field == 'hp':
            table.hp = request.POST['value'] if request.POST['value'] != '' else None

        table.save()
        skill.save()

        return HttpResponse('sucess')

    return HttpResponse('fail')


# ficha do personagem
@never_cache
def player_token_creation_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':

        # criação do personagem
        character_form = CharacterForm(request.POST)
        if character_form.is_valid:
            character = character_form.save(commit=False)
            character.owner = request.user
            character.portrait = request.FILES.get('portrait')

            if request.POST['allocated_campaign']:
                campaign = Campaign.objects.get(id=int(request.POST['allocated_campaign']))
                campaign.team.add(request.user)

            character.save()

        character_id = character.id

        # atributos e modificadores
        atributes_form = AtributesForm(request.POST)
        if atributes_form.is_valid:
            atributes = atributes_form.save(commit=False)
            atributes.owner = Character.objects.get(id=character_id)
            atributes.save()

        # habilidades
        skills_form = SkillsForm(request.POST)
        if skills_form.is_valid:
            skills = skills_form.save(commit=False)
            skills.owner = Character.objects.get(id=character_id)
            skills.save()

        # caracteristicas
        characteristics_form = CharacteristicsForm(request.POST)
        if characteristics_form.is_valid:
            characteristics = characteristics_form.save(commit=False)
            characteristics.owner = Character.objects.get(id=character_id)
            characteristics.hp = characteristics.hp_max
            characteristics.save()

        # ataques
        attacks = request.POST.get('attacks')

        if attacks:
            attacks = json.loads(attacks.strip())

        for attack_dict in attacks:
            attack = AttackForm(attack_dict)
            if attack.is_valid:
                attack_commit = attack.save(commit=False)
                attack_commit.owner = Character.objects.get(id=character_id)
                attack_commit.save()

        return redirect('/player_selection/')
    
    invited_campaigns = Campaign.objects.filter(
        team=request.user
    )

    user_campaigns = Campaign.objects.filter(
        owner=request.user
    )

    return render(request, 'new_character.html', {
        'invited_campaigns': invited_campaigns.union(user_campaigns)
    })

# jogar com personagem
@never_cache
def character_play_view(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    character = Character.objects.get(id=id)
    if character.allocated_campaign is not None:
        campaign  = Campaign.objects.get(id=character.allocated_campaign.id)

        if character.owner != request.user and campaign.owner != request.user:
            return  HttpResponse('Permissão não concedida')
        
    else:
        if character.owner != request.user:
            return  HttpResponse('Permissão não concedida')

    atributes = Atributes.objects.get(owner=character.id)
    skills = Skills.objects.get(owner=character.id)
    characteristics = Characteristics.objects.get(owner=character.id)

    attacks = Attack.objects.filter(owner=character.id)

    character.id = hash_id(character.id)

    response = {
        'character': character,
        'atributes': atributes,
        'skills': skills,
        'characteristics': characteristics,
        'attacks': attacks
    }

    if character.allocated_campaign is not None:
        character.allocated_campaign.id = hash_id(character.allocated_campaign.id)
        response['campaign'] = character.allocated_campaign
    else:
        response['campaign'] = None

    return render(request, 'character_play.html', response)


# sessão de editar personagem
def view_edit_token(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    character = Character.objects.get(id=id)

    if character.owner != request.user:
        return  HttpResponse('Permissão não concedida')

    atributes = Atributes.objects.get(owner=character.id)
    skills = Skills.objects.get(owner=character.id)
    characteristics = Characteristics.objects.get(owner=character.id)

    attacks = Attack.objects.filter(owner=character.id)

    if request.method == 'POST':
        character_form = CharacterForm(request.POST, instance=character)
        if character_form.is_valid():
            character_commit = character_form.save(commit=False)

            if request.FILES:
                character_commit.portrait = request.FILES.get('portrait')

            if request.POST['allocated_campaign']:
                campaign = Campaign.objects.get(id=int(request.POST['allocated_campaign']))
                campaign.team.add(request.user)
            else:
                if character_commit.allocated_campaign:
                    character_commit.allocated_campaign = None

            character_commit.save()

        atributes_form = AtributesForm(request.POST, instance=atributes)
        if atributes_form.is_valid():
            atributes_form.save()

        skills_form = SkillsForm(request.POST, instance=skills)
        if skills_form.is_valid():
            skills_form.save()

        characteristics_form = CharacteristicsForm(
            request.POST, instance=characteristics)
        if characteristics_form.is_valid():
            characteristics_form.save()

        all_attacks = request.POST.get('attacks')
        if all_attacks:
            all_attacks = json.loads(all_attacks)

            for attack_dict in all_attacks:
                if attack_dict['created']:
                    attack = Attack.objects.get(id=attack_dict['id'])
                    attack_form = AttackForm(attack_dict, instance=attack)

                    if attack_form.is_valid():
                        attack_form.save()

                else:
                    attack_form = AttackForm(attack_dict)

                    if attack_form.is_valid():
                        attack = attack_form.save(commit=False)
                        attack.owner = Character.objects.get(id=character.id)
                        attack.save()

        all_attacks_remove = request.POST.get('remove_attacks')
        if all_attacks_remove:
            all_attacks_remove = json.loads(all_attacks_remove)

            for attack_dict in all_attacks_remove:
                attack = Attack.objects.get(id=attack_dict)
                if attack.owner == character:
                    attack.delete()

        return redirect('/player_selection/')

    else:

        invited_campaigns = Campaign.objects.filter(
            team=request.user
        )

        user_campaigns = Campaign.objects.filter(
            owner=request.user
        )

        return render(request, 'edit_character.html', {
            'character': character,
            'atributes': atributes,
            'skills': skills,
            'characteristics': characteristics,
            'attacks': attacks,
            'invited_campaigns': invited_campaigns.union(user_campaigns)
        })

# seleção de campanha
@never_cache
def campaign_selection_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # pesquisa
    if request.GET.get('search'):
        search_input = request.GET['search_input']
        campaigns = Campaign.objects.filter(
            owner=request.user.id,
            name__icontains=search_input
        )

    else:
        campaigns = Campaign.objects.filter(owner=request.user)

    for campaign in campaigns:
        campaign.id = hash_id(campaign.id)

    return render(request, 'campaign_selection.html', {
        'campaigns': campaigns
    })


# criação de campanha
@never_cache
def campaign_creation_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    # Criação da campanha
    if request.method == 'POST':
        campaignForm = CampaignForm(request.POST)
        if campaignForm.is_valid():
            campaign = campaignForm.save(commit=False)
            campaign.owner = request.user
            campaign.cover = request.FILES.get('cover')
            campaign.save()

            if request.POST['team']:
                team_ids = json.loads(request.POST['team'])
                team_users = User.objects.filter(id__in=team_ids)

                campaign.team.set(team_users)

            return redirect('/campaign_selection/')
        else:
            print(f'Erro ao salvar campanha: {campaignForm.errors}')

    # pesquisa
    if request.GET.get('search'):
        search_input = request.GET['search_input']
        players = User.objects.filter(
            name__icontains=search_input
        )

        return JsonResponse({
            'players': json.dumps(list(players.values()))
        })

    else:
        return render(request, 'campaign_creation.html')


# pesquisar usuários
def userSearch(request):
    if request.method == 'GET':
        search = request.GET['search']
        players = None

        if request.GET.get('search'):
            players = User.objects.filter(
                username__icontains=search
            ).exclude(username=request.user.username)

        return JsonResponse({
            'players': list(players.values()) if players else []
        })


# edição de campanha
@never_cache
def campaign_edit_view(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    campaign = Campaign.objects.get(id=id)

    if campaign.owner != request.user:
        return HttpResponse('Permissão não concedida')

    if request.method == 'POST':
        campaignForm = CampaignForm(request.POST, instance=campaign)

        if campaignForm.is_valid():
            campaign_commit = campaignForm.save(commit=False)
            
            if request.FILES:
                campaign_commit.cover = request.FILES.get('cover')

            if request.POST['removedUsers']:
                removedUsers = json.loads(request.POST['removedUsers'])
                for rmUser in removedUsers:
                    user = User.objects.get(id=rmUser)
                    campaign_commit.team.remove(user)

                    characters_in_campaign = Character.objects.filter(owner=user, allocated_campaign=campaign)
                    print(characters_in_campaign)
                    for character in characters_in_campaign:
                        character.allocated_campaign = None
                        character.save()

                
            if request.POST['newUsers']:
                newUsers = json.loads(request.POST['newUsers'])
                for newUser in newUsers:
                    user = User.objects.get(id=newUser)
                    campaign_commit.team.add(user)

            campaign_commit.save()
            return redirect('/campaign_selection/')

    usersInCampaign = campaign.team.all()

    return render(request, 'campaign_edit.html', {
        'campaign': campaign,
        'users': usersInCampaign
    })

# deleção de campanha
@never_cache
def campaign_delete_view(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    campaign = Campaign.objects.get(id=id)

    characters = Character.objects.filter(allocated_campaign=campaign)

    for character in characters:
        character.allocated_campaign = None
        character.save()

    if campaign.owner == request.user:
        campaign.delete()
    else:
        return HttpResponse('Permissão não concedida')

    return redirect('/campaign_selection/')

# manejamento de campanha
@never_cache
def campaig_manage_view(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    campaign = Campaign.objects.get(id=id)

    if campaign.owner != request.user:
        return HttpResponse('Permissão não concedida')

    charactersInCampaign = Character.objects.filter(allocated_campaign=campaign)
    entitysInCampaign = Entity.objects.filter(owner=campaign)

    for character in charactersInCampaign:
        character.id = hash_id(character.id)

    for entity in entitysInCampaign:
        atributes = Atributes.objects.get(entity_owner=entity.id)
        skills = Skills.objects.get(entity_owner=entity.id)
        characteristics = Characteristics.objects.get(entity_owner=entity.id)

        attacks = Attack.objects.filter(entity_owner=entity.id)

        serialized_attributes = serializers.serialize('json', [atributes])
        serialized_skills = serializers.serialize('json', [skills])
        serialized_characteristics = serializers.serialize('json', [characteristics])
        serialized_attacks = serializers.serialize('json', attacks)

        attributes_data = json.loads(serialized_attributes)[0]['fields']
        skills_data = json.loads(serialized_skills)[0]['fields']
        characteristics_data = json.loads(serialized_characteristics)[0]['fields']
        attacks_data = [item['fields'] for item in json.loads(serialized_attacks)]

        character_data = {
            "attributes": attributes_data,
            "skills": skills_data,
            "characteristics": characteristics_data,
            "attacks": attacks_data
        }

        character_json = json.dumps(character_data)

        entity.token = character_json
        entity.id = hash_id(entity.id)

    campaign.id = hash_id(campaign.id)

    return render(request, 'campaign_manage.html', {
        'campaign': campaign,
        'characters': charactersInCampaign,
        'entitys': entitysInCampaign
    })


# enviar mensagem
@csrf_exempt
def send_message(request, campaign, character):
    campaign_id = campaign.split('-')[0]
    if character != 'master':
        character_id = character.split('-')[0]

    if not check_hash(campaign) and not check_hash(character):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    if request.method == 'POST':
        campaign = Campaign.objects.get(id=campaign_id)
        content = request.POST['content']

        if character != 'master':
            character = Character.objects.get(id=character_id)

        messageCommit = Message()

        if character != 'master':
            messageCommit.owner = character
            messageCommit.username = character.name
        
        messageCommit.campaign = campaign
        messageCommit.content = content
        messageCommit.save()

    return HttpResponse('success')

# adquirir mensagem
def get_message(request, campaign):
    if not check_hash(campaign):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    id = campaign.split('-')[0]
    campaign = Campaign.objects.get(id=id)
    
    messages = Message.objects.filter(campaign=campaign)

    for message in messages:
        try:
            character = Character.objects.get(id=message.owner)
            message.owner = character.name
        except:
            pass

    return JsonResponse({
        'payload': list(messages.values())
    })

# criar nova entidade
@never_cache
def new_entity_view(request, hash):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    if request.method == 'POST':
        entity_form = EntityForm(request.POST)
        if entity_form.is_valid:
            entity = entity_form.save(commit=False)
            entity.owner = Campaign.objects.get(id=id)
            entity.portrait = request.FILES.get('portrait')

            entity.save()

        entity_id = entity.id

        # atributos e modificadores
        atributes_form = AtributesForm(request.POST)
        if atributes_form.is_valid:
            atributes = atributes_form.save(commit=False)
            atributes.entity_owner = Entity.objects.get(id=entity_id)
            atributes.save()

        # habilidades
        skills_form = SkillsForm(request.POST)
        if skills_form.is_valid:
            skills = skills_form.save(commit=False)
            skills.entity_owner = Entity.objects.get(id=entity_id)
            skills.save()

        # caracteristicas
        characteristics_form = CharacteristicsForm(request.POST)
        if characteristics_form.is_valid:
            characteristics = characteristics_form.save(commit=False)
            characteristics.entity_owner = Entity.objects.get(id=entity_id)
            characteristics.hp = characteristics.hp_max
            characteristics.save()

        # ataques
        attacks = request.POST.get('attacks')

        if attacks:
            attacks = json.loads(attacks.strip())

        for attack_dict in attacks:
            attack = AttackForm(attack_dict)
            if attack.is_valid:
                attack_commit = attack.save(commit=False)
                attack_commit.entity_owner = Entity.objects.get(id=entity_id)
                attack_commit.save()
        
        return redirect(f'/campaign_manage/{hash}/')
    
    return render(request, 'new_entity.html')


# salvamento automático da campanha
@csrf_exempt
def campaign_autosave(request, hash, field):
    if not request.user.is_authenticated:
        return redirect('/login/')

    id = hash.split('-')[0]

    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    if request.method == 'POST':
        table = Campaign.objects.get(id=id)

        if table.owner != request.user.id:
            return HttpResponse('Permissão não concedida')

        if field == 'notes':
            table.notes = request.POST['value']
        elif field == 'history':
            table.history = request.POST['value']

        table.save()

        return HttpResponse('200')
    
    return HttpResponse('303')


# deleção de personagem
def entity_delete(request, entity, campaign):
    if not request.user.is_authenticated:
        return redirect('/login/')

    entity_id = entity.split('-')[0]

    if not check_hash(entity):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    this_campaign = Campaign.objects.get(id=int(campaign.split('-')[0]))

    if this_campaign.owner != request.user:
        return HttpResponse('Permissão não concedida')
    
    entityCommit = Entity.objects.get(id=entity_id)
    entityCommit.delete()

    return redirect(f'/campaign_manage/{campaign}/')


#  edição de entidade
@never_cache
def entity_edit_view(request, entity, campaign):
    if not request.user.is_authenticated:
        return redirect('/login/')

    entity_id = entity.split('-')[0]

    if not check_hash(entity):
        return HttpResponseNotFound('Personagem não encontrado.')
    
    entity_campaign = Campaign.objects.get(id=int(campaign.split('-')[0]))

    if entity_campaign.owner != request.user:
        return HttpResponse('Permissão não concedida')
    
    entity = Entity.objects.get(id=entity_id)
    atributes = Atributes.objects.get(entity_owner=entity)
    skills = Skills.objects.get(entity_owner=entity)
    characteristics = Characteristics.objects.get(entity_owner=entity)

    attacks = Attack.objects.filter(entity_owner=entity)

    if request.method == 'POST':
        entity_form = EntityForm(request.POST, instance=entity)
        if entity_form.is_valid():
            entity_commit = entity_form.save(commit=False)

            if request.FILES:
                entity_commit.portrait = request.FILES.get('portrait')

            entity_commit.save()

        atributes_form = AtributesForm(request.POST, instance=atributes)
        if atributes_form.is_valid():
            atributes_form.save()

        skills_form = SkillsForm(request.POST, instance=skills)
        if skills_form.is_valid():
            skills_form.save()

        characteristics_form = CharacteristicsForm(request.POST, instance=characteristics)
        if characteristics_form.is_valid():
            characteristics_form.save()

        all_attacks = request.POST.get('attacks')
        if all_attacks:
            all_attacks = json.loads(all_attacks)

            for attack_dict in all_attacks:
                if attack_dict['created']:
                    attack = Attack.objects.get(id=attack_dict['id'])
                    attack_form = AttackForm(attack_dict, instance=attack)

                    if attack_form.is_valid():
                        attack_form.save()

                else:
                    attack_form = AttackForm(attack_dict)

                    if attack_form.is_valid():
                        attack = attack_form.save(commit=False)
                        attack.entity_owner = Entity.objects.get(id=entity_id)
                        attack.save()

        all_attacks_remove = request.POST.get('remove_attacks')
        if all_attacks_remove:
            all_attacks_remove = json.loads(all_attacks_remove)

            for attack_dict in all_attacks_remove:
                attack = Attack.objects.get(id=attack_dict)
                if attack.entity_owner == entity:
                    attack.delete()

        return redirect(f'/campaign_manage/{campaign}')

    else:

        return render(request, 'entity_edit.html', {
            'entity': entity,
            'atributes': atributes,
            'skills': skills,
            'characteristics': characteristics,
            'attacks': attacks,
        })