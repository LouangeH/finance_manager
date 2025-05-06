from django.db import models

class CategorieRevenue(models.Model):
    categorie = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.categorie}"