from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import BuildingForm
from collections import defaultdict
from .models import User, Building, Resource, Village, VillageBuilding, Troop, VillageTroop
from django.db.models import F
from .utils_views import *
from .utils_tasks import *
from decimal import Decimal
import math


def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save()
            return redirect(reverse('add_building'))
    else:
        form = BuildingForm()
    return render(request, 'travian/add_building.html', {'form': form})

def home(request):
    return render(request, 'travian/home.html')

@login_required
def build_building(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)
        village = get_object_or_404(Village, user=request.user)
        error_message = validate_building_constraints(selected_building, village)

        if error_message:
            messages.error(request, error_message)
        else:
            if check_and_deduct_resources(selected_building, village, 0):
                existing_building_count = village.village_buildings.filter(building=selected_building).count()
                new_name = generate_building_name(selected_building, existing_building_count + 1)
                resource = create_resource(selected_building, village)
                create_village_building(village, selected_building, resource, new_name)
                update_population(village)
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_resource'))

    return render(request, 'travian/build_resource.html', {'available_buildings': Building.objects.all()})

@login_required
def build_infrastructure(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)
        village = get_object_or_404(Village, user=request.user)

        if village.village_buildings.filter(building=selected_building).exists():
            messages.error(request, f"You already have a {selected_building.name}. You cannot build another one.")
        else:
            if check_and_deduct_resources(selected_building, village, 0):
                village_building = create_village_infrastructure(village, selected_building, name=selected_building.name)
                update_population(village)
                update_village_resource_capacity(selected_building, village_building)  # Updated this line
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_infrastructure'))

    available_buildings = Building.objects.filter(b_type='Infrastructure')
    return render(request, 'travian/build_infrastructure.html', {'available_buildings': available_buildings})

@login_required
def build_infantry(request):
    village = get_object_or_404(Village, user=request.user)

    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)

        if village.village_buildings.filter(building=selected_building).exists():
            messages.error(request, f"You already have a {selected_building.name}. You cannot build another one.")
        else:
            if check_and_deduct_resources(selected_building, village, 0):
                village_building = create_village_infrastructure(village, selected_building, name=selected_building.name)
                update_population(village)
                update_village_resource_capacity(selected_building, village_building)
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_infantry'))

    available_buildings = Building.objects.filter(b_type='Military')

    return render(request, 'travian/build_infantry.html', {'available_buildings': available_buildings})

@login_required
def upgrade_building(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_select')
        if building_id:
            village_building = get_object_or_404(VillageBuilding, id=building_id)
            selected_building = village_building.building
            village = village_building.village
            current_level = village_building.level

            if current_level >= 10:
                messages.error(request, 'Building is already at its maximum level.')
            elif check_and_deduct_resources(selected_building, village, current_level):
                new_level = upgrade_building_level(village_building)

                if selected_building.b_type == 'Resource':
                    update_resource_generation_rate(village_building)
                elif selected_building.name in ('Granary', 'Warehouse'):
                    update_village_resource_capacity(selected_building, village_building)

                update_population(village)
                messages.success(request, 'Building successfully upgraded.')
            else:
                messages.error(request, 'Insufficient resources to upgrade.')

    return render(request, 'travian/upgrade_building.html', {'messages': messages.get_messages(request)})

@login_required
def troop_building(request):
    village = get_object_or_404(Village, user=request.user)
    barracks = Building.objects.get(name='Barracks')
    stable = Building.objects.get(name="Stable")
    stable_level = village.village_buildings.get(building=stable).level if village.village_buildings.filter(building=stable).exists() else 0
    barracks_level = village.village_buildings.get(building=barracks).level if village.village_buildings.filter(building=barracks).exists() else 0
    available_troops = Troop.objects.all()
    if request.method == 'POST':
        selected_troop_id = request.POST.get('troop_id')
        quantity = int(request.POST.get('quantity', 0))

        try:
            selected_troop = Troop.objects.get(id=selected_troop_id)
            total_cost = calculate_troop_cost(selected_troop.construction_cost, quantity)
        except Troop.DoesNotExist:
            messages.error(request, 'Selected troop does not exist')
            return redirect(reverse('troop_building'))

        if quantity <= 0:
            messages.error(request, 'Wrong quantity selected')
            return redirect(reverse('troop_building'))

        if not check_village_resources(total_cost, village):
            messages.error(request, 'Insufficient resources to build troops.')
            return redirect(reverse('troop_building'))

        deduct_resources(total_cost, village)
        village_troop, _ = VillageTroop.objects.get_or_create(village=village, troop=selected_troop)
        village_troop.quantity += quantity
        village_troop.save()

        return redirect(reverse('troop_building'))

    return render(request, 'travian/troop_building.html', {'barracks_level': barracks_level, 'stable_level': stable_level, 'available_troops': available_troops})

def player_list(request):
    players = User.objects.all()  # Retrieve all players
    context = {'players': players}
    return render(request, 'travian/player_list.html', context)

def attack_view(request, player_id):
    player = get_object_or_404(User, id=player_id)
    attacked_village = player.village.first()  # Assuming a player has only one village, retrieve the first village
    logged_village = get_object_or_404(Village, user=request.user)
    troops = logged_village.village_troops.all()  # Fetch troops associated with the village
    defender_troops = attacked_village.village_troops.all()
    original_defender_troops = list(defender_troops)


    if request.method == 'POST':
        selected_troops = {}  # Store the selected troop quantities
        total_carrying_capacity = 0  # Total carrying capacity of the attack

        for troop in troops:
            quantity = int(request.POST.get(f'troop_quantity_{troop.id}', 0))
            selected_troops[troop] = quantity
        attacker_cavalry_attack_power = sum(troop.troop.attack * quantity for troop, quantity in selected_troops.items() if troop.troop.t_type == 'Cavalry')
        attacker_infantry_attack_power = sum(troop.troop.attack * quantity for troop, quantity in selected_troops.items() if troop.troop.t_type == 'Infantry')
        attacker_total_attack_power = attacker_cavalry_attack_power + attacker_infantry_attack_power
        defender_cavalry_defense_power = sum(defender_troop.troop.cavalry_defense * defender_troop.quantity for defender_troop in defender_troops)
        defender_infantry_defense_power = sum(defender_troop.troop.defense * defender_troop.quantity for defender_troop in defender_troops)
        defender_total_defense_power = (defender_cavalry_defense_power * (attacker_cavalry_attack_power / attacker_total_attack_power)) + (defender_infantry_defense_power * (attacker_infantry_attack_power / attacker_total_attack_power))
        if attacker_total_attack_power >= defender_total_defense_power:
            # Attacker wins
            loser_strength = defender_total_defense_power
            winner_strength = attacker_total_attack_power
            loser_troops = defender_troops
            losing_troops = defender_troops
            winner_troops = selected_troops
            winner_casualties_percent = ((loser_strength / winner_strength) ** 1.5) * 100
        else:
            # Defender wins
            loser_strength = attacker_total_attack_power
            winner_strength = defender_total_defense_power
            loser_troops = selected_troops
            winner_troops = {}
            for troop in defender_troops:
                winner_troops[troop] = troop.quantity
            winner_casualties_percent = ((loser_strength / winner_strength) ** 1.5) * 100

        if attacker_total_attack_power > defender_total_defense_power:
            # Attacker wins
            dead_troops_list = []
            for troop, quantity in selected_troops.items():
                surviving_quantity = math.ceil(quantity * (1 - winner_casualties_percent / 100))
                remaining_quantity = max(surviving_quantity, 0)  # Ensure the quantity doesn't go below zero
                dead_troops = quantity - remaining_quantity
                dead_troops_list.append(dead_troops)
                troop.quantity = troop.quantity - dead_troops
                troop.save()
                total_carrying_capacity += troop.troop.carrying_capacity * remaining_quantity
            
            # Calculate the stolen resource amounts
            wood_amount = total_carrying_capacity / 4
            clay_amount = total_carrying_capacity / 4
            iron_amount = total_carrying_capacity / 4
            crop_amount = total_carrying_capacity / 4

            wood_amount = min(attacked_village.wood_amount, Decimal(wood_amount))
            clay_amount = min(attacked_village.clay_amount, Decimal(clay_amount))
            iron_amount = min(attacked_village.iron_amount, Decimal(iron_amount))
            crop_amount = min(attacked_village.crop_amount, Decimal(crop_amount))

            total_stolen_amount = wood_amount + clay_amount + iron_amount + crop_amount

            attacked_village.wood_amount -= wood_amount
            attacked_village.clay_amount -= clay_amount
            attacked_village.iron_amount -= iron_amount
            attacked_village.crop_amount -= crop_amount
            attacked_village.save()

            logged_village.wood_amount += wood_amount
            logged_village.clay_amount += clay_amount
            logged_village.iron_amount += iron_amount
            logged_village.crop_amount += crop_amount
            logged_village.save()
            defender_troops.delete()
            print(original_defender_troops)
            return render(request, 'travian/attack_win_result.html', {
            'attacked_village': attacked_village,
            'selected_troops': selected_troops,
            'casualties': dead_troops_list,
            'original_deffender': original_defender_troops,
            'attacker_total_attack_power': winner_strength,
            'defender_troops': losing_troops,
            'defender_total_defense_power': defender_total_defense_power,
            'wood_amount': wood_amount,
            'clay_amount': clay_amount,
            'iron_amount': iron_amount,
            'crop_amount': crop_amount,
            'total_stolen_amount': total_stolen_amount,
            'total_carrying_capacity': total_carrying_capacity,
        })

        else:
            # Defender wins
            dead_troops_list = []
            for troop, quantity in winner_troops.items():
                surviving_quantity = math.ceil(troop.quantity * (1 - winner_casualties_percent / 100))
                remaining_quantity = max(surviving_quantity, 0) 
                dead_troops = quantity - remaining_quantity
                dead_troops_list.append(dead_troops)
                troop.quantity = troop.quantity - dead_troops
                troop.save()
            
            for troop, quantity in loser_troops.items():
                troop.quantity -= quantity
                troop.save()

        logged_village.wood_amount = min(logged_village.wood_amount, logged_village.warehouse_capacity)
        logged_village.clay_amount = min(logged_village.clay_amount, logged_village.warehouse_capacity)
        logged_village.iron_amount = min(logged_village.iron_amount, logged_village.warehouse_capacity)
        logged_village.crop_amount = min(logged_village.crop_amount, logged_village.granary_capacity)
        logged_village.save()
        return render(request, 'travian/attack_lose_result.html', {
            'attacked_village': attacked_village,
            'selected_troops': selected_troops,
            'original_deffender': original_defender_troops,
            'deffender_total_attack_power': winner_strength,
            'attacker_total_defense_power': attacker_total_attack_power,
            'total_carrying_capacity': total_carrying_capacity,
            'casualties': dead_troops_list,
        })
    
    return render(request, 'travian/attack.html', {'player': player, 'attacked_village': attacked_village, 'troops': troops})

def generate_building_name(building, count):
    return f"{building.name} {count}"


