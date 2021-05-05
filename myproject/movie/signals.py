from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=UserProfile, dispatch_uid='create_user')
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(instance.username)
        user.set_password(instance.password)
        user.save()


@receiver(post_delete, sender=StudentProfile, dispatch_uid='delete_user')
def delete_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.username).delete()
