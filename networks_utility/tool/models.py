from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

class MyUserMangager(BaseUserManager):
    def create_user(self,email,password):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(
            email = self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    objects = MyUserMangager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class ClientRecipient(models.Model):
    id = models.AutoField(primary_key=True)
    client_email = models.EmailField()
    recipient_email = models.EmailField()
    region = models.CharField(max_length=20,default='APAC')

    class Meta:
        unique_together = ('client_email', 'recipient_email')
        verbose_name = 'Client-Recipient Pair'
        verbose_name_plural = 'Client-Recipient Pairs'

    def __str__(self):
        return f"\nClient: {self.client_email}, \nRecipient: {self.recipient_email}, \nRegion: {self.region}\n"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watched_clients = models.ManyToManyField(ClientRecipient, blank=True)

    def __str__(self):
        return f"Profile for user: {self.user}"
