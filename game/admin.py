from django.contrib import admin
from .models import (
    PokemonSpecies, UserProfile, UserPokemon,
    Battle, Item, UserItem
)

@admin.register(PokemonSpecies)
class PokemonSpeciesAdmin(admin.ModelAdmin):
    list_display = ['pokedex_id', 'name', 'type1', 'type2', 'rarity', 'base_stat_total']
    list_filter = ['type1', 'type2', 'rarity']
    search_fields = ['name', 'pokedex_id']
    ordering = ['pokedex_id']

    fieldsets = (
        ('Basic Info', {
            'fields': ('pokedex_id', 'name', 'type1', 'type2', 'rarity', 'sprite_url')
        }),
        ('Base Stats', {
            'fields': ('base_hp', 'base_attack', 'base_defense',
                      'base_sp_attack', 'base_sp_defense', 'base_speed')
        }),
        ('Game Mechanics', {
            'fields': ('catch_rate', 'evolution_level', 'evolves_from')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['trainer_name', 'user', 'level', 'experience', 'coins', 'total_pokemon_caught']
    list_filter = ['level']
    search_fields = ['trainer_name', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Trainer Info', {
            'fields': ('user', 'trainer_name', 'level', 'experience')
        }),
        ('Resources', {
            'fields': ('coins', 'pokeballs', 'great_balls', 'ultra_balls', 'master_balls')
        }),
        ('Daily Limits', {
            'fields': ('daily_catches',)
        }),
        ('Statistics', {
            'fields': ('total_pokemon_caught', 'battles_won', 'battles_lost')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserPokemon)
class UserPokemonAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'species', 'owner', 'level', 'iv_percentage', 'is_shiny']
    list_filter = ['species__type1', 'species__type2', 'level', 'is_shiny', 'is_favorite']
    search_fields = ['nickname', 'species__name', 'owner__username']
    readonly_fields = ['caught_at', 'updated_at', 'max_hp', 'total_stats', 'iv_percentage']

    fieldsets = (
        ('Basic Info', {
            'fields': ('owner', 'species', 'nickname', 'level', 'experience')
        }),
        ('Individual Values', {
            'fields': ('iv_hp', 'iv_attack', 'iv_defense',
                      'iv_sp_attack', 'iv_sp_defense', 'iv_speed', 'iv_percentage')
        }),
        ('Status', {
            'fields': ('current_hp', 'max_hp', 'is_shiny', 'is_favorite')
        }),
        ('Battle Stats', {
            'fields': ('battles_won', 'battles_lost', 'total_stats')
        }),
        ('Timestamps', {
            'fields': ('caught_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'battle_type', 'player_pokemon', 'opponent_pokemon', 'status', 'created_at']
    list_filter = ['battle_type', 'status', 'created_at']
    search_fields = ['trainer__username', 'player_pokemon__nickname', 'opponent_pokemon__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'price']
    list_filter = ['item_type']
    search_fields = ['name']

@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity']
    list_filter = ['item__item_type']
    search_fields = ['user__username', 'item__name']

