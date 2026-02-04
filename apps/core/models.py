from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Az e-mail lesz az elsődleges azonosító a username helyett
    email = models.EmailField(unique=True)
    
    # Itt adhatsz hozzá később extra mezőket (pl. egyenleg, hűségpont)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # A Django adminnak még kell a username

    def __str__(self):
        return self.email