from django.db import models

class Anime(models.Model):
    mal_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100,null=False,blank=False)
    score = models.FloatField(null=False,blank=False)
    genres = models.TextField(null=False,blank=False)
    sypnopsis = models.TextField()
    group = models.CharField(max_length=10,null=False,blank=False)
    popularity = models.IntegerField(null=False,blank=False)
    
    def __str__(self):
        return self.name

class AnimeAll(models.Model):
    mal_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100,null=False,blank=False)
    score = models.FloatField(null=False,blank=False)
    genres = models.TextField(null=False,blank=False)
    sypnopsis = models.TextField()
    group = models.CharField(max_length=10,null=False,blank=False)
    popularity = models.IntegerField(null=False,blank=False)
    members = models.IntegerField(null=False,blank=False)
    favorites = models.IntegerField(null=False,blank=False)    

    def __str__(self):
        return self.name

