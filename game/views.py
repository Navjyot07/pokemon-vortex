from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import random
import json
import time

from .models import (
    PokemonSpecies, UserProfile, UserPokemon,
    Battle, Item, UserItem
)

def dashboard(request):
    """Main dashboard view"""
    if not request.user.is_authenticated:
        return render(request, 'game/landing.html')

    profile = request.user.userprofile
    recent_pokemon = UserPokemon.objects.filter(owner=request.user)[:6]

    context = {
        'profile': profile,
        'recent_pokemon': recent_pokemon,
    }
    return render(request, 'game/dashboard.html', context)

@login_required
def pokemon_list(request):
    """List user's Pokemon"""
    pokemon = UserPokemon.objects.filter(owner=request.user)

    # Filter by type if specified
    type_filter = request.GET.get('type')
    if type_filter:
        pokemon = pokemon.filter(
            Q(species__type1=type_filter) | Q(species__type2=type_filter)
        )

    # Sort options
    sort_by = request.GET.get('sort', 'caught_at')
    if sort_by == 'level':
        pokemon = pokemon.order_by('-level')
    elif sort_by == 'name':
        pokemon = pokemon.order_by('species__name')
    elif sort_by == 'iv':
        # This would need a custom ordering in a real app
        pokemon = pokemon.order_by('-caught_at')
    else:
        pokemon = pokemon.order_by('-caught_at')

    context = {
        'pokemon': pokemon,
        'current_type': type_filter,
        'current_sort': sort_by,
    }
    return render(request, 'game/pokemon_list.html', context)

@login_required
def pokemon_detail(request, pokemon_id):
    """Pokemon detail view"""
    pokemon = get_object_or_404(UserPokemon, id=pokemon_id, owner=request.user)

    context = {
        'pokemon': pokemon,
    }
    return render(request, 'game/pokemon_detail.html', context)

# @login_required
# def catch_pokemon(request):
#     """Catch wild Pokemon"""
#     profile = request.user.userprofile

#     # Check daily catch limit
#     today = timezone.now().date()
#     if profile.last_catch_reset != today:
#         profile.daily_catches = 0
#         profile.last_catch_reset = today
#         profile.save()

#     if profile.daily_catches >= 50:  # Daily limit
#         if request.headers.get('HX-Request'):
#             return HttpResponse('<div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> You\'ve reached your daily catch limit!</div>')
#         messages.error(request, "You've reached your daily catch limit!")
#         return redirect('game:dashboard')

#     # Check if user has pokeballs
#     if profile.pokeballs <= 0:
#         if request.headers.get('HX-Request'):
#             return HttpResponse('<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> You don\'t have any Pokeballs! <a href="/shop/" class="alert-link">Buy more</a></div>')
#         messages.error(request, "You don't have any Pokeballs!")
#         return redirect('game:shop')

#     if request.method == 'POST':
#         # Prevent double submissions by checking if a catch was already processed in this session
#         last_catch_time = request.session.get('last_catch_time', 0)
#         current_time = time.time()

#         # Prevent catches within 2 seconds of each other
#         if current_time - last_catch_time < 2:
#             if request.headers.get('HX-Request'):
#                 return HttpResponse('<div class="alert alert-info"><i class="fas fa-clock"></i> Please wait before searching again...</div>')
#             return redirect('game:catch_pokemon')

#         # Update last catch time
#         request.session['last_catch_time'] = current_time

#         # Attempt to catch a random Pokemon
#         all_species = list(PokemonSpecies.objects.all())
#         if not all_species:
#             if request.headers.get('HX-Request'):
#                 return HttpResponse('<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> No Pokemon species available!</div>')
#             messages.error(request, "No Pokemon species available!")
#             return redirect('game:dashboard')

#         # Weighted random selection based on rarity
#         rarity_weights = {
#             'common': 50,
#             'uncommon': 25,
#             'rare': 15,
#             'epic': 7,
#             'legendary': 2,
#             'mythical': 1
#         }

#         weighted_species = []
#         for species in all_species:
#             weight = rarity_weights.get(species.rarity, 1)
#             weighted_species.extend([species] * weight)

#         wild_pokemon = random.choice(weighted_species)
#         wild_level = random.randint(1, min(profile.level + 5, 50))

#         # Calculate catch chance
#         catch_rate = wild_pokemon.catch_rate
#         level_modifier = max(0.1, 1 - (wild_level - profile.level) * 0.05)
#         catch_chance = (catch_rate / 255) * level_modifier

#         # Use pokeball
#         profile.pokeballs -= 1

#         if random.random() < catch_chance:
#             # Successful catch!
#             caught_pokemon = UserPokemon.objects.create(
#                 owner=request.user,
#                 species=wild_pokemon,
#                 level=wild_level
#             )
#             profile.daily_catches += 1
#             profile.total_pokemon_caught += 1
#             profile.add_experience(wild_level * 10)
#             profile.save()

#             if request.headers.get('HX-Request'):
#                 return HttpResponse(f'''
#                     <div class="alert alert-success">
#                         <h5><i class="fas fa-check-circle"></i> Congratulations!</h5>
#                         <p class="mb-2">You caught a Level {wild_level} {wild_pokemon.name}!</p>
#                         <div class="d-flex gap-2">
#                             <a href="/pokemon/{caught_pokemon.id}/" class="btn btn-primary btn-sm">
#                                 <i class="fas fa-eye"></i> View Pokemon
#                             </a>
#                             <button class="btn btn-success btn-sm" onclick="location.reload()">
#                                 <i class="fas fa-search"></i> Search Again
#                             </button>
#                         </div>
#                     </div>
#                 ''')
#             messages.success(request, f"Congratulations! You caught a Level {wild_level} {wild_pokemon.name}!")
#             return redirect('game:pokemon_detail', pokemon_id=caught_pokemon.id)
#         else:
#             # Pokemon escaped
#             profile.save()
#             if request.headers.get('HX-Request'):
#                 return HttpResponse(f'''
#                     <div class="alert alert-warning">
#                         <h5><i class="fas fa-exclamation-triangle"></i> Oh no!</h5>
#                         <p class="mb-2">The wild Level {wild_level} {wild_pokemon.name} escaped!</p>
#                         <button class="btn btn-warning btn-sm" onclick="location.reload()">
#                             <i class="fas fa-search"></i> Try Again
#                         </button>
#                     </div>
#                 ''')
#             messages.warning(request, f"The wild {wild_pokemon.name} escaped!")

#     context = {
#         'profile': profile,
#     }
#     return render(request, 'game/catch.html', context)

@login_required
def battle_wild(request):
    """Start a battle with wild Pokemon"""
    user_pokemon = UserPokemon.objects.filter(owner=request.user, current_hp__gt=0)

    if not user_pokemon.exists():
        messages.error(request, "You need healthy Pokemon to battle!")
        return redirect('game:pokemon_list')

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        selected_pokemon = get_object_or_404(UserPokemon, id=pokemon_id, owner=request.user)

        if selected_pokemon.current_hp <= 0:
            messages.error(request, "That Pokemon is fainted!")
            return redirect('game:battle_wild')

        # Create a wild opponent
        all_species = list(PokemonSpecies.objects.all())
        if not all_species:
            messages.error(request, "No Pokemon species available!")
            return redirect('game:dashboard')

        wild_species = random.choice(all_species)
        wild_level = random.randint(max(1, selected_pokemon.level - 5), selected_pokemon.level + 5)

        # Create battle
        battle = Battle.objects.create(
            trainer=request.user,
            battle_type='wild',
            player_pokemon=selected_pokemon,
            opponent_pokemon=wild_species,
            opponent_level=wild_level
        )

        battle.add_to_log(f"A wild {wild_species.name} appeared!")
        battle.add_to_log(f"Go, {selected_pokemon.display_name}!")

        return redirect('game:battle_detail', battle_id=battle.id)

    context = {
        'user_pokemon': user_pokemon,
    }
    return render(request, 'game/battle_start.html', context)

@login_required
def battle_detail(request, battle_id):
    """Battle detail view"""
    battle = get_object_or_404(Battle, id=battle_id, trainer=request.user)

    if battle.status != 'ongoing':
        # Battle is finished, show results
        context = {
            'battle': battle,
            'battle_log': json.loads(battle.battle_log) if battle.battle_log else [],
        }
        return render(request, 'game/battle_result.html', context)

    context = {
        'battle': battle,
        'battle_log': json.loads(battle.battle_log) if battle.battle_log else [],
    }
    return render(request, 'game/battle.html', context)

@login_required
def battle_action(request, battle_id):
    """Handle battle actions via HTMX"""
    battle = get_object_or_404(Battle, id=battle_id, trainer=request.user)

    if battle.status != 'ongoing':
        return JsonResponse({'error': 'Battle is not ongoing'})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'attack':
            # Simple battle system
            player_pokemon = battle.player_pokemon
            opponent_level = battle.opponent_level

            # Calculate damage (simplified)
            player_attack = player_pokemon.attack_stat
            base_damage = random.randint(10, 30) + (player_attack // 10)

            battle.turns += 1
            battle.add_to_log(f"{player_pokemon.display_name} attacks for {base_damage} damage!")

            # Opponent attacks back (simplified)
            opponent_attack = random.randint(20, 40) + opponent_level
            damage_to_player = max(1, opponent_attack - (player_pokemon.defense_stat // 10))

            player_pokemon.current_hp = max(0, player_pokemon.current_hp - damage_to_player)
            player_pokemon.save()

            battle.add_to_log(f"Wild {battle.opponent_pokemon.name} attacks for {damage_to_player} damage!")

            # Check battle end conditions
            if player_pokemon.current_hp <= 0:
                battle.status = 'lost'
                battle.add_to_log(f"{player_pokemon.display_name} fainted!")
                battle.add_to_log("You lost the battle!")

                # Update profile stats
                profile = request.user.userprofile
                profile.battles_lost += 1
                profile.save()

            elif random.random() < 0.3:  # 30% chance opponent faints
                battle.status = 'won'
                battle.add_to_log(f"Wild {battle.opponent_pokemon.name} fainted!")
                battle.add_to_log("You won the battle!")

                # Rewards
                exp_gained = opponent_level * 15
                coins_gained = opponent_level * 5

                battle.experience_gained = exp_gained
                battle.coins_gained = coins_gained

                # Update Pokemon and profile
                player_pokemon.battles_won += 1
                player_pokemon.save()

                profile = request.user.userprofile
                profile.battles_won += 1
                profile.coins += coins_gained
                profile.add_experience(exp_gained)

                battle.add_to_log(f"Gained {exp_gained} experience and {coins_gained} coins!")

            battle.save()

        elif action == 'flee':
            battle.status = 'fled'
            battle.add_to_log("You fled from the battle!")
            battle.save()

    # Return updated battle state for HTMX
    context = {
        'battle': battle,
        'battle_log': json.loads(battle.battle_log) if battle.battle_log else [],
    }
    return render(request, 'game/battle_partial.html', context)

@login_required
def profile(request):
    """User profile view"""
    profile = request.user.userprofile
    pokemon_count = UserPokemon.objects.filter(owner=request.user).count()

    context = {
        'profile': profile,
        'pokemon_count': pokemon_count,
    }
    return render(request, 'game/profile.html', context)

@login_required
def shop(request):
    """Shop view"""
    profile = request.user.userprofile

    if request.method == 'POST':
        item_type = request.POST.get('item')
        quantity = int(request.POST.get('quantity', 1))

        prices = {
            'pokeball': 200,
            'great_ball': 600,
            'ultra_ball': 1200,
        }

        if item_type in prices:
            total_cost = prices[item_type] * quantity

            if profile.coins >= total_cost:
                profile.coins -= total_cost

                if item_type == 'pokeball':
                    profile.pokeballs += quantity
                elif item_type == 'great_ball':
                    profile.great_balls += quantity
                elif item_type == 'ultra_ball':
                    profile.ultra_balls += quantity

                profile.save()
                messages.success(request, f"Purchased {quantity} {item_type.replace('_', ' ').title()}(s)!")
            else:
                messages.error(request, "Not enough coins!")

    context = {
        'profile': profile,
    }
    return render(request, 'game/shop.html', context)


@login_required
def wild_map(request):
    """Wild Pokemon map interface"""
    profile = request.user.userprofile
    pokemon_count = UserPokemon.objects.filter(owner=request.user).count()

    # Check daily catch limit
    today = timezone.now().date()
    if profile.last_catch_reset != today:
        profile.daily_catches = 0
        profile.last_catch_reset = today
        profile.save()

    context = {
        'profile': profile,
        'pokemon_count': pokemon_count,
    }
    return render(request, 'game/wild_map.html', context)

@login_required
def encounter_pokemon(request):
    """Generate a random Pokemon encounter for the map"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    profile = request.user.userprofile

    # Check if user has pokeballs
    if profile.pokeballs <= 0:
        return JsonResponse({'success': False, 'message': "You don't have any Pokeballs!"})

    # Check daily catch limit
    today = timezone.now().date()
    if profile.last_catch_reset != today:
        profile.daily_catches = 0
        profile.last_catch_reset = today
        profile.save()

    if profile.daily_catches >= 50:
        return JsonResponse({'success': False, 'message': "You've reached your daily catch limit!"})

    # Get all Pokemon species
    all_species = list(PokemonSpecies.objects.all())
    if not all_species:
        return JsonResponse({'success': False, 'message': 'No Pokemon species available!'})

    # Weighted random selection based on rarity
    rarity_weights = {
        'common': 50,
        'rare': 25,
        'epic': 15,
        'legendary': 5,
        'ultrabeast': 1,
        'mythical': 1,
    }

    weighted_species = []
    for species in all_species:
        weight = rarity_weights.get(species.rarity, 1)
        weighted_species.extend([species] * weight)

    wild_pokemon = random.choice(weighted_species)
    wild_level = random.randint(1, min(profile.level + 5, 50))

    # Store encounter in session for catch attempt
    request.session['current_encounter'] = {
        'species_id': wild_pokemon.id,
        'level': wild_level,
        'timestamp': time.time()
    }

    return JsonResponse({
        'success': True,
        'pokemon': {
            'id': wild_pokemon.id,
            'name': wild_pokemon.name,
            'level': wild_level,
            'rarity': wild_pokemon.rarity
        }
    })

@login_required
def attempt_catch(request):
    """Attempt to catch the encountered Pokemon"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    profile = request.user.userprofile

    # Get encounter from session
    encounter = request.session.get('current_encounter')
    if not encounter:
        return JsonResponse({'success': False, 'message': 'No active encounter!'})

    # Check if encounter is still valid (within 5 minutes)
    if time.time() - encounter['timestamp'] > 300:
        del request.session['current_encounter']
        return JsonResponse({'success': False, 'message': 'Encounter expired!'})

    # Check if user has pokeballs
    if profile.pokeballs <= 0:
        return JsonResponse({'success': False, 'message': "You don't have any Pokeballs!"})

    # Get the Pokemon species
    try:
        wild_pokemon = PokemonSpecies.objects.get(id=encounter['species_id'])
    except PokemonSpecies.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid Pokemon species!'})

    wild_level = encounter['level']

    # Calculate catch chance
    catch_rate = wild_pokemon.catch_rate
    level_modifier = max(0.1, 1 - (wild_level - profile.level) * 0.05)
    catch_chance = (catch_rate / 255) * level_modifier

    # Use pokeball
    profile.pokeballs -= 1

    if random.random() < catch_chance:
        # Successful catch!
        caught_pokemon = UserPokemon.objects.create(
            owner=request.user,
            species=wild_pokemon,
            level=wild_level,
            iv_hp=random.randint(0, 31),
            iv_attack=random.randint(0, 31),
            iv_defense=random.randint(0, 31),
            iv_speed=random.randint(0, 31),
        )

        profile.daily_catches += 1

        # Award experience and coins
        exp_gained = wild_level * 10
        coins_gained = wild_level * 5

        profile.experience += exp_gained
        profile.coins += coins_gained

        # Check for level up
        level_up = False
        while profile.experience >= profile.level * 1000:
            profile.experience -= profile.level * 1000
            profile.level += 1
            level_up = True

        profile.save()

        # Clear encounter
        del request.session['current_encounter']

        pokemon_count = UserPokemon.objects.filter(owner=request.user).count()

        message = f"Caught {wild_pokemon.name} (Level {wild_level})!"
        if level_up:
            message += f" You leveled up to Level {profile.level}!"

        return JsonResponse({
            'success': True,
            'message': message,
            'pokeballs': profile.pokeballs,
            'daily_catches': profile.daily_catches,
            'pokemon_count': pokemon_count,
            'exp_gained': exp_gained,
            'coins_gained': coins_gained
        })
    else:
        # Failed catch
        profile.save()

        return JsonResponse({
            'success': False,
            'message': f"{wild_pokemon.name} broke free!",
            'pokeballs': profile.pokeballs,
            'daily_catches': profile.daily_catches
        })

