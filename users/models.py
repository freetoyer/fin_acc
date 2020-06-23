from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
 
 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    name = models.CharField('name', max_length=50)
    phone = models.CharField('phone', max_length=16)
 
    def __str__(self):
        return f"{self.user.pk}-{self.user.email}"
   
@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_update_profile")
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
