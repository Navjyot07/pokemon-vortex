from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from game.models import UserProfile
        # Generate a unique trainer name
        base_name = instance.username or f"Trainer{instance.id}"
        trainer_name = base_name
        counter = 1
        
        while UserProfile.objects.filter(trainer_name=trainer_name).exists():
            trainer_name = f"{base_name}{counter}"
            counter += 1
        
        UserProfile.objects.create(
            user=instance,
            trainer_name=trainer_name
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except:
        # Profile doesn't exist, create it
        create_user_profile(sender, instance, True, **kwargs)

