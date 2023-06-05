from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
from .functions import *
from .hash import *

import json

# redirecionar para uma view
def redirect_view(request):
    if request.user.is_authenticated:
        return redirect('/selection/')
    else:
        return redirect('/login/')

# login
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

# seleção de conta
def selection_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        return render(request, 'selection.html')

# seleção de personagens
def player_selection_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    user_id = request.user.id

    # pesquisa
    if request.GET.get('search'):
        search_input = request.GET['search_input']
        all_characters = Character.objects.filter(
            owner=user_id,
            name__icontains=search_input
        )

    else:
        all_characters = Character.objects.filter(owner=user_id)

    # trocar id por hash
    for character in all_characters:
        character.id = hash_id(character.id)

    return render(request, 'character_selection.html', {
        'all_characters': all_characters
    })


def delete_character(request, hash):
    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    id = hash.split('-')[0]

    character = Character.objects.get(id=id)
    character.delete()

    return redirect('/player_selection/')

# autosave do personagem
@csrf_exempt
def character_autosave(request, hash, field):
    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    id = hash.split('-')[0]

    character = Character.objects.get(id=id)
    table = Characteristics.objects.get(owner=character.id)
    skill = Skills.objects.get(owner=character.id)

    if request.method == 'POST':
        if field == 'inspiration':
            skill.inspiration = request.POST['value']

        elif field == 'class_armor_temp':
            table.class_armor_temp = request.POST['value']

        elif field == 'displacement_temp':
            table.displacement_temp = request.POST['value']

        elif field == 'hp_temp':
            table.hp_temp = request.POST['value']

        elif field == 'pc':
            table.pc = request.POST['value']

        elif field == 'pp':
            table.pp = request.POST['value']

        elif field == 'po':
            table.po = request.POST['value']

        elif field == 'pl':
            table.pl = request.POST['value']

        elif field == 'da':
            table.da = request.POST['value']

        elif field == 'equipments':
            table.equipments = request.POST['value']

        elif field == 'inventory':
            table.inventory = request.POST['value']

        elif field == 'history':
            table.history = request.POST['value']

        elif field == 'hp':
            table.hp = request.POST['value']

        table.save()
        skill.save()

        return HttpResponse('sucess')

    return HttpResponse('fail')

# ficha do personagem
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
        else:
            print(skills_form.errors)

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
            attack = Attack()

            attack.owner = Character.objects.get(id=character_id)
            attack.name = attack_dict['name']

            attack.magic_lvl = attack_dict['magic_lvl']

            attack.dice_1 = attack_dict['dice_1']
            attack.dice_2 = attack_dict['dice_2']
            attack.dice_3 = attack_dict['dice_3']

            attack.roll_1 = attack_dict['roll_1'] or None
            attack.roll_2 = attack_dict['roll_2'] or None
            attack.roll_3 = attack_dict['roll_3'] or None

            attack.damage_modifier = attack_dict['damage_modifier'] or None
            attack.attribute_modifier = attack_dict['attribute_modifier']

            attack.proficiency = attack_dict['proficiency']

            attack.description = attack_dict['description']

            attack.type = attack_dict['type']

            attack.save()

        return redirect('/player_selection/')

    return render(request, 'new_character.html')


def character_play_view(request, hash):
    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    id = hash.split('-')[0]

    character = Character.objects.get(id=id)

    atributes = Atributes.objects.get(owner=character.id)
    skills = Skills.objects.get(owner=character.id)
    characteristics = Characteristics.objects.get(owner=character.id)

    attacks = Attack.objects.filter(owner=character.id)

    character.id = hash_id(character.id)

    return render(request, 'character_play.html', {
        'character': character,
        'atributes': atributes,
        'skills': skills,
        'characteristics': characteristics,
        'attacks': attacks
    })


def view_edit_token(request, hash):
    if not check_hash(hash):
        return HttpResponseNotFound('Personagem não encontrado.')

    id = hash.split('-')[0]

    character = Character.objects.get(id=id)
    atributes = Atributes.objects.get(owner=character.id)
    skills = Skills.objects.get(owner=character.id)
    characteristics = Characteristics.objects.get(owner=character.id)

    attacks = Attack.objects.filter(owner=character.id)

    if request.method == 'POST':
        character_form = CharacterForm(request.POST, instance=character)
        if character_form.is_valid():
            character_commit = character_form.save(commit=False)
            
            if request.FILES:
                character_commit.portrait =  request.FILES.get('portrait')
            
            character_commit.save()

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
        return render(request, 'edit_character.html', {
            'character': character,
            'atributes': atributes,
            'skills': skills,
            'characteristics': characteristics,
            'attacks': attacks
        })


def campaign_creation_view(request):
    return render(request, 'campaign_creation.html')
