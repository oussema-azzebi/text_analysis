from django.db import models



class Person(models.Model):
    """
    Person model
    """
    name = models.CharField(max_length=255, null=False)
    occupation = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    birthday = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    nationality = models.CharField(max_length=255, null=True)
    image_link = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name

class Frequency(models.Model):
    """
    Frequency model
    """
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    freq = models.PositiveSmallIntegerField(default=0)
