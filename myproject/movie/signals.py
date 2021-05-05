from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = UserProfile(username=instance.username, email=instance.email)
        # user.set_password(instance.password)
        user.save()


@receiver(post_delete, sender=User, dispatch_uid='delete_user_profile')
def delete_user_profile(sender, instance, **kwargs):
    UserProfile.nodes.filter(username=instance.username).delete()
