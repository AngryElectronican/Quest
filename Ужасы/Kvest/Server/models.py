from django.db import models

class Kvest(models.Model):

    name=models.CharField(max_length=50)
    status_1=models.IntegerField(default=0)
    status_2=models.IntegerField(default=0)
    status_3=models.IntegerField(default=0)
    status_4=models.IntegerField(default=0)
    status_5=models.IntegerField(default=0)
    status_6=models.IntegerField(default=0)

    def __str__(self):
        return self.name
