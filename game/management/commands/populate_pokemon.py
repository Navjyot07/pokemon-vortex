from django.core.management.base import BaseCommand
from game.models import PokemonSpecies, Item

class Command(BaseCommand):
    help = 'Populate database with initial Pokemon and items'
    
    def handle(self, *args, **options):
        self.stdout.write('Populating Pokemon species...')
        
        # Create some starter Pokemon
        pokemon_data = [
            {
                'pokedex_id': 1,
                'name': 'Bulbasaur',
                'type1': 'Grass',
                'type2': 'Poison',
                'base_hp': 45,
                'base_attack': 49,
                'base_defense': 49,
                'base_sp_attack': 65,
                'base_sp_defense': 65,
                'base_speed': 45,
                'rarity': 'uncommon',
                'catch_rate': 45,
                'evolution_level': 16,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
            },
            {
                'pokedex_id': 2,
                'name': 'Ivysaur',
                'type1': 'Grass',
                'type2': 'Poison',
                'base_hp': 60,
                'base_attack': 62,
                'base_defense': 63,
                'base_sp_attack': 80,
                'base_sp_defense': 80,
                'base_speed': 60,
                'rarity': 'rare',
                'catch_rate': 45,
                'evolution_level': 32,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png'
            },
            {
                'pokedex_id': 3,
                'name': 'Venusaur',
                'type1': 'Grass',
                'type2': 'Poison',
                'base_hp': 80,
                'base_attack': 82,
                'base_defense': 83,
                'base_sp_attack': 100,
                'base_sp_defense': 100,
                'base_speed': 80,
                'rarity': 'epic',
                'catch_rate': 45,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png'
            },
            {
                'pokedex_id': 4,
                'name': 'Charmander',
                'type1': 'Fire',
                'base_hp': 39,
                'base_attack': 52,
                'base_defense': 43,
                'base_sp_attack': 60,
                'base_sp_defense': 50,
                'base_speed': 65,
                'rarity': 'uncommon',
                'catch_rate': 45,
                'evolution_level': 16,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'
            },
            {
                'pokedex_id': 5,
                'name': 'Charmeleon',
                'type1': 'Fire',
                'base_hp': 58,
                'base_attack': 64,
                'base_defense': 58,
                'base_sp_attack': 80,
                'base_sp_defense': 65,
                'base_speed': 80,
                'rarity': 'rare',
                'catch_rate': 45,
                'evolution_level': 36,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png'
            },
            {
                'pokedex_id': 6,
                'name': 'Charizard',
                'type1': 'Fire',
                'type2': 'Flying',
                'base_hp': 78,
                'base_attack': 84,
                'base_defense': 78,
                'base_sp_attack': 109,
                'base_sp_defense': 85,
                'base_speed': 100,
                'rarity': 'epic',
                'catch_rate': 45,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png'
            },
            {
                'pokedex_id': 7,
                'name': 'Squirtle',
                'type1': 'Water',
                'base_hp': 44,
                'base_attack': 48,
                'base_defense': 65,
                'base_sp_attack': 50,
                'base_sp_defense': 64,
                'base_speed': 43,
                'rarity': 'uncommon',
                'catch_rate': 45,
                'evolution_level': 16,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'
            },
            {
                'pokedex_id': 8,
                'name': 'Wartortle',
                'type1': 'Water',
                'base_hp': 59,
                'base_attack': 63,
                'base_defense': 80,
                'base_sp_attack': 65,
                'base_sp_defense': 80,
                'base_speed': 58,
                'rarity': 'rare',
                'catch_rate': 45,
                'evolution_level': 36,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/8.png'
            },
            {
                'pokedex_id': 9,
                'name': 'Blastoise',
                'type1': 'Water',
                'base_hp': 79,
                'base_attack': 83,
                'base_defense': 100,
                'base_sp_attack': 85,
                'base_sp_defense': 105,
                'base_speed': 78,
                'rarity': 'epic',
                'catch_rate': 45,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png'
            },
            {
                'pokedex_id': 25,
                'name': 'Pikachu',
                'type1': 'Electric',
                'base_hp': 35,
                'base_attack': 55,
                'base_defense': 40,
                'base_sp_attack': 50,
                'base_sp_defense': 50,
                'base_speed': 90,
                'rarity': 'rare',
                'catch_rate': 190,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'
            },
            {
                'pokedex_id': 150,
                'name': 'Mewtwo',
                'type1': 'Psychic',
                'base_hp': 106,
                'base_attack': 110,
                'base_defense': 90,
                'base_sp_attack': 154,
                'base_sp_defense': 90,
                'base_speed': 130,
                'rarity': 'legendary',
                'catch_rate': 3,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png'
            },
            {
                'pokedex_id': 151,
                'name': 'Mew',
                'type1': 'Psychic',
                'base_hp': 100,
                'base_attack': 100,
                'base_defense': 100,
                'base_sp_attack': 100,
                'base_sp_defense': 100,
                'base_speed': 100,
                'rarity': 'mythical',
                'catch_rate': 45,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png'
            },
            # Add some common Pokemon
            {
                'pokedex_id': 16,
                'name': 'Pidgey',
                'type1': 'Normal',
                'type2': 'Flying',
                'base_hp': 40,
                'base_attack': 45,
                'base_defense': 40,
                'base_sp_attack': 35,
                'base_sp_defense': 35,
                'base_speed': 56,
                'rarity': 'common',
                'catch_rate': 255,
                'evolution_level': 18,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/16.png'
            },
            {
                'pokedex_id': 19,
                'name': 'Rattata',
                'type1': 'Normal',
                'base_hp': 30,
                'base_attack': 56,
                'base_defense': 35,
                'base_sp_attack': 25,
                'base_sp_defense': 35,
                'base_speed': 72,
                'rarity': 'common',
                'catch_rate': 255,
                'evolution_level': 20,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/19.png'
            },
            {
                'pokedex_id': 10,
                'name': 'Caterpie',
                'type1': 'Bug',
                'base_hp': 45,
                'base_attack': 30,
                'base_defense': 35,
                'base_sp_attack': 20,
                'base_sp_defense': 20,
                'base_speed': 45,
                'rarity': 'common',
                'catch_rate': 255,
                'evolution_level': 7,
                'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10.png'
            },
        ]
        
        created_count = 0
        for data in pokemon_data:
            pokemon, created = PokemonSpecies.objects.get_or_create(
                pokedex_id=data['pokedex_id'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created {pokemon.name}')
        
        # Set up evolution chains
        try:
            bulbasaur = PokemonSpecies.objects.get(pokedex_id=1)
            ivysaur = PokemonSpecies.objects.get(pokedex_id=2)
            venusaur = PokemonSpecies.objects.get(pokedex_id=3)
            
            ivysaur.evolves_from = bulbasaur
            ivysaur.save()
            venusaur.evolves_from = ivysaur
            venusaur.save()
            
            charmander = PokemonSpecies.objects.get(pokedex_id=4)
            charmeleon = PokemonSpecies.objects.get(pokedex_id=5)
            charizard = PokemonSpecies.objects.get(pokedex_id=6)
            
            charmeleon.evolves_from = charmander
            charmeleon.save()
            charizard.evolves_from = charmeleon
            charizard.save()
            
            squirtle = PokemonSpecies.objects.get(pokedex_id=7)
            wartortle = PokemonSpecies.objects.get(pokedex_id=8)
            blastoise = PokemonSpecies.objects.get(pokedex_id=9)
            
            wartortle.evolves_from = squirtle
            wartortle.save()
            blastoise.evolves_from = wartortle
            blastoise.save()
            
        except PokemonSpecies.DoesNotExist:
            pass
        
        self.stdout.write(f'Created {created_count} new Pokemon species')
        
        # Create basic items
        self.stdout.write('Creating items...')
        items_data = [
            {
                'name': 'Pokeball',
                'item_type': 'pokeball',
                'description': 'A basic ball for catching Pokemon',
                'price': 200,
            },
            {
                'name': 'Great Ball',
                'item_type': 'pokeball',
                'description': 'A better ball with higher catch rate',
                'price': 600,
            },
            {
                'name': 'Ultra Ball',
                'item_type': 'pokeball',
                'description': 'An excellent ball with very high catch rate',
                'price': 1200,
            },
            {
                'name': 'Potion',
                'item_type': 'potion',
                'description': 'Restores 20 HP to a Pokemon',
                'price': 300,
            },
            {
                'name': 'Super Potion',
                'item_type': 'potion',
                'description': 'Restores 50 HP to a Pokemon',
                'price': 700,
            },
        ]
        
        item_count = 0
        for data in items_data:
            item, created = Item.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                item_count += 1
                self.stdout.write(f'Created {item.name}')
        
        self.stdout.write(f'Created {item_count} new items')
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database!')
        )

