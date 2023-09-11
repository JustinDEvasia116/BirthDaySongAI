from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os
# Create your models here.

class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    otp = models.CharField(max_length=100, blank=True, null=True)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)

    
    
    def __str__(self):
        return self.user.username


class Profiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    mood = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=20, blank=True, null=True)
    generated_lyrics = models.CharField(blank=True, null=True)
    petname = models.CharField(blank=True, null=True)
    angry = models.CharField(blank=True, null=True)
    funny = models.CharField(blank=True, null=True)
    movie = models.CharField(blank=True, null=True)
    sport = models.CharField(blank=True, null=True)
    smile = models.CharField(blank=True, null=True)
    audio_file = models.FileField(upload_to='assets/audiofiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name
    
    @property
    def audio_file_url(self):
        if self.audio_file:
            return self.audio_file.url
        return None

@receiver(post_delete, sender=Profiles)
def post_delete_profile(sender, instance, **kwargs):
    try:
        if instance.audio_file:
            if os.path.exists(instance.audio_file.path):
                os.remove(instance.audio_file.path)
    except Exception as e:
        pass

@receiver(pre_save, sender=Profiles)
def pre_save_profile(sender, instance, **kwargs):
    try:
        if instance.pk:  # Check if this is an update
            old_instance = Profiles.objects.get(pk=instance.pk)
            if old_instance.audio_file and old_instance.audio_file != instance.audio_file:
                if os.path.exists(old_instance.audio_file.path):
                    os.remove(old_instance.audio_file.path)
    except Exception as e:
        pass
