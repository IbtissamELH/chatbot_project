from django.db import models

class Interaction(models.Model):
    question = models.TextField()
    reponse = models.TextField()
    solution = models.TextField()
    date = models.DateTimeField(auto_now_add=True)