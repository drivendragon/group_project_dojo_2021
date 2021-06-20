from django.db import models
from datetime import datetime
import re, bcrypt

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="first name must be longer than 2 characters"
        if len(postdata['f_n'])<2:
            errors['l_n']="last name must be longer than 2 characters" 
        if not email_check.match(postdata['email']):
            errors['email']="email must be valid format"
        if len(postdata['pw'])<8:
            errors['pw']="password must be at least 8 characters"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw']="password and confirm password must match"
        return errors




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_testimony = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    
class GroupManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['group_name']) < 3:
            errors['group_name'] = "Group name must be at least 3 characters long."
        if len(postData['description']) < 1:
            errors['description'] = "You must ender a description."
        if len(postData['prayer_list']) < 1:
            errors['prayer_list'] = "Let the group know what to pray about!"
        return errors
    
class Group(models.Model):
    group_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prayer_list = models.TextField()
    users_in_this_group = models.ManyToManyField(User, related_name="users_groups")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = GroupManager()
    
class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='group_messages', on_delete=models.CASCADE)
    
class Prayer(models.Model):
    fk_user=models.ForeignKey(User, related_name='fk_user', on_delete=models.CASCADE)
    fk_group=models.ForeignKey(User, related_name='fk_group', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
