from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pokemon/', views.pokemon_list, name='pokemon_list'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),
    # path('catch/', views.catch_pokemon, name='catch_pokemon'),
    path('wild-map/', views.wild_map, name='wild_map'),
    path('catch/encounter/', views.encounter_pokemon, name='encounter_pokemon'),
    path('catch/attempt/', views.attempt_catch, name='attempt_catch'),
    path('battle/', views.battle_wild, name='battle_wild'),
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    path('battle/<int:battle_id>/action/', views.battle_action, name='battle_action'),
    path('profile/', views.profile, name='profile'),
    path('shop/', views.shop, name='shop'),
]

