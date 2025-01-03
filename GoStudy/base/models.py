from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=250)

class Room(models.Model):
    host  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic  = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    # participants = 
    updated = models.DateTimeField(auto_now = True) # take a snap shot every single time 
    created = models.DateTimeField(auto_now_add = True) # take a snap shot when saved or create 
    # id = 

# use of the class == table 
# wherer var == Column's of the table
# row == instances of the class
# i.e  name, description, updated, created is the column_name
class Meta:
    ordering = ['-updated', '-created']
    # recent activity and the thing it first called ordering
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null = True)

    # when room is deleted so all child of what , if set_null so messga ein db, or cascade == deleted child
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True) # take a snap shot every single time 
    created = models.DateTimeField(auto_now_add = True) # take a snap shot when saved or create 

    def __str__(self):
        return self.body[0:50]
    

    # one to many relations like insta