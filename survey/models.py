from django.db import models

# Create your models here.
class Token(models.Model):
    session_token = models.CharField(editable=False, blank=True, null=True, max_length=64)

class Survey(models.Model):
    title = models.CharField(max_length=256,default="")
    description = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.title

class Question(models.Model):
    text = models.CharField(max_length=1000,default="")
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    