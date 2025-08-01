from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import json

class PokemonSpecies(models.Model):
    """Base Pokemon species data"""
    pokedex_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=20)
    type2 = models.CharField(max_length=20, blank=True, null=True)
    base_hp = models.IntegerField()
    base_attack = models.IntegerField()
    base_defense = models.IntegerField()
    base_sp_attack = models.IntegerField()
    base_sp_defense = models.IntegerField()
    base_speed = models.IntegerField()
    sprite_url = models.URLField(blank=True, null=True)
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
        ('mythical', 'Mythical'),
        ('ultrabeast', 'UltraBeast'),
    ], default='common')
    catch_rate = models.IntegerField(default=45, validators=[MinValueValidator(1), MaxValueValidator(255)])
    evolution_level = models.IntegerField(null=True, blank=True)
    evolves_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='evolutions')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Pokemon Species"
        ordering = ['pokedex_id']

    def __str__(self):
        return f"#{self.pokedex_id:03d} {self.name}"

    @property
    def base_stat_total(self):
        return (self.base_hp + self.base_attack + self.base_defense +
                self.base_sp_attack + self.base_sp_defense + self.base_speed)

class UserProfile(models.Model):
    """Extended user profile for the game"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer_name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    coins = models.IntegerField(default=1000)
    pokeballs = models.IntegerField(default=10)
    great_balls = models.IntegerField(default=5)
    ultra_balls = models.IntegerField(default=2)
    master_balls = models.IntegerField(default=0)

    # Daily limits
    daily_catches = models.IntegerField(default=0)
    last_catch_reset = models.DateField(auto_now_add=True)

    # Stats
    total_pokemon_caught = models.IntegerField(default=0)
    battles_won = models.IntegerField(default=0)
    battles_lost = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer_name} (Level {self.level})"

    @property
    def win_rate(self):
        total_battles = self.battles_won + self.battles_lost
        if total_battles == 0:
            return 0
        return round((self.battles_won / total_battles) * 100, 2)

    def add_experience(self, exp):
        """Add experience and handle level ups"""
        self.experience += exp
        # Simple leveling: every 1000 exp = 1 level
        new_level = (self.experience // 1000) + 1
        if new_level > self.level:
            self.level = new_level
            # Give rewards for leveling up
            self.coins += new_level * 100
            self.pokeballs += 5
        self.save()

class UserPokemon(models.Model):
    """Individual Pokemon owned by users"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemon')
    species = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    experience = models.IntegerField(default=0)

    # hp = models.IntegerField(default=10)
    # attack = models.IntegerField(default=5)
    # defense = models.IntegerField(default=5)
    # speed = models.IntegerField(default=5)
    # max_hp = models.IntegerField(default=10)


    # Individual Values (IVs) - 0-31 for each stat
    iv_hp = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])
    iv_attack = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])
    iv_defense = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])
    iv_sp_attack = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])
    iv_sp_defense = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])
    iv_speed = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(31)])

    # Status
    current_hp = models.IntegerField()
    is_shiny = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    # Battle stats
    battles_won = models.IntegerField(default=0)
    battles_lost = models.IntegerField(default=0)

    caught_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-caught_at']

    def save(self, *args, **kwargs):
        # Generate random IVs if this is a new Pokemon
        if not self.pk:
            self.iv_hp = random.randint(0, 31)
            self.iv_attack = random.randint(0, 31)
            self.iv_defense = random.randint(0, 31)
            self.iv_sp_attack = random.randint(0, 31)
            self.iv_sp_defense = random.randint(0, 31)
            self.iv_speed = random.randint(0, 31)

            # 1/4096 chance for shiny
            self.is_shiny = random.randint(1, 4096) == 1

            # Set current HP to max HP
            self.current_hp = self.max_hp

        super().save(*args, **kwargs)

    def __str__(self):
        name = self.nickname if self.nickname else self.species.name
        return f"{name} (Lv.{self.level})"

    @property
    def display_name(self):
        return self.nickname if self.nickname else self.species.name

    @property
    def max_hp(self):
        """Calculate max HP based on base stats, IVs, and level"""
        base = self.species.base_hp
        iv = self.iv_hp
        level = self.level
        return int(((2 * base + iv) * level / 100) + level + 10)

    @property
    def attack_stat(self):
        base = self.species.base_attack
        iv = self.iv_attack
        level = self.level
        return int(((2 * base + iv) * level / 100) + 5)

    @property
    def defense_stat(self):
        base = self.species.base_defense
        iv = self.iv_defense
        level = self.level
        return int(((2 * base + iv) * level / 100) + 5)

    @property
    def sp_attack_stat(self):
        base = self.species.base_sp_attack
        iv = self.iv_sp_attack
        level = self.level
        return int(((2 * base + iv) * level / 100) + 5)

    @property
    def sp_defense_stat(self):
        base = self.species.base_sp_defense
        iv = self.iv_sp_defense
        level = self.level
        return int(((2 * base + iv) * level / 100) + 5)

    @property
    def speed_stat(self):
        base = self.species.base_speed
        iv = self.iv_speed
        level = self.level
        return int(((2 * base + iv) * level / 100) + 5)

    @property
    def total_stats(self):
        return (self.max_hp + self.attack_stat + self.defense_stat +
                self.sp_attack_stat + self.sp_defense_stat + self.speed_stat)

    @property
    def iv_percentage(self):
        """Calculate IV percentage (perfect IVs = 100%)"""
        total_ivs = (self.iv_hp + self.iv_attack + self.iv_defense +
                    self.iv_sp_attack + self.iv_sp_defense + self.iv_speed)
        return round((total_ivs / 186) * 100, 1)  # 186 = 31 * 6

    def heal(self):
        """Fully heal the Pokemon"""
        self.current_hp = self.max_hp
        self.save()

    def can_evolve(self):
        """Check if Pokemon can evolve"""
        if not self.species.evolution_level:
            return False
        return self.level >= self.species.evolution_level

    def evolve(self):
        """Evolve the Pokemon if possible"""
        if not self.can_evolve():
            return False

        # Find evolution
        evolution = self.species.evolutions.first()
        if evolution:
            self.species = evolution
            self.save()
            return True
        return False

class Battle(models.Model):
    """Battle records"""
    BATTLE_TYPES = [
        ('wild', 'Wild Pokemon'),
        ('trainer', 'Trainer Battle'),
        ('gym', 'Gym Battle'),
    ]

    BATTLE_STATUS = [
        ('ongoing', 'Ongoing'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('fled', 'Fled'),
    ]

    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battles')
    battle_type = models.CharField(max_length=20, choices=BATTLE_TYPES)
    status = models.CharField(max_length=20, choices=BATTLE_STATUS, default='ongoing')

    # Pokemon involved
    player_pokemon = models.ForeignKey(UserPokemon, on_delete=models.CASCADE, related_name='battles_as_player')
    opponent_pokemon = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    opponent_level = models.IntegerField(default=5)

    # Battle data
    turns = models.IntegerField(default=0)
    battle_log = models.TextField(default='[]')  # JSON string of battle events

    # Rewards
    experience_gained = models.IntegerField(default=0)
    coins_gained = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.username} vs {self.opponent_pokemon.name} ({self.status})"

    def add_to_log(self, message):
        """Add a message to the battle log"""
        log = json.loads(self.battle_log) if self.battle_log else []
        log.append({
            'turn': self.turns,
            'message': message,
            'timestamp': str(self.updated_at)
        })
        self.battle_log = json.dumps(log)
        self.save()

class Item(models.Model):
    """Game items"""
    ITEM_TYPES = [
        ('pokeball', 'Pokeball'),
        ('potion', 'Potion'),
        ('berry', 'Berry'),
        ('stone', 'Evolution Stone'),
        ('misc', 'Miscellaneous'),
    ]

    name = models.CharField(max_length=100, unique=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    description = models.TextField()
    price = models.IntegerField(default=0)
    sprite_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    """Items owned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ['user', 'item']

    def __str__(self):
        return f"{self.user.username} - {self.item.name} x{self.quantity}"

