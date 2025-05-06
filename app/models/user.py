from django.db import models
from django.contrib.auth.models import User

# Pour suivre les utilisateurs si besoin
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tu peux ajouter plus de champs ici

    def __str__(self):
        return self.user.username
