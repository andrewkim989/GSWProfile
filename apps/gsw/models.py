from __future__ import unicode_literals
from django.db import models

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')
number_regex = re.compile(r'[0-9]+$')


class UserManager(models.Manager):

    def register_validate(self, postData):
        errors = {}
        a = User.objects.filter(email = postData['email'])
        
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        elif not name_regex.match(postData['first_name']):
            errors["first_name"] = "First name should contain only letters."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        elif not name_regex.match(postData['last_name']):
            errors["last_name"] = "Last name should contain only letters."

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid e-mail address."
        elif a:
            errors["email"] = "The email already exists in our system. Please type another one."

        if len(postData['password']) < 1:
            errors["password"] = "Please enter your password."
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters long."
        elif re.search('[0-9]', postData['password']) is None:
            errors["password"] = "Make sure that your password has a number in it." 
        elif re.search('[A-Z]', postData['password']) is None: 
            errors["password"] = "Make sure that your password has a capital letter in it."
        
        if len(postData["password_con"]) < 1:
            errors["password_con"] = "Please verify your password."
        elif postData["password_con"] != postData['password']:
            errors["password_con"] = "The passwords do not match."
        return errors
    
    def login_validate(self, postData):
        user = User.objects.filter(email = postData['email'])
        errors = {}

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid e-mail address."
        if len(postData['password']) < 1:
            errors["password"] = "Please enter your password."
        elif len(user) == 0:
            errors["password"] = "Cannot find e-mail address in our system. Please register."
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors["password"] = "Incorrect password. Please try again."

        return errors

    def player_validate(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Name must be more than two characters long"
        
        if not number_regex.match(postData['birth_month']):
            errors['birth_month'] = "Birth month should contain only numbers."
        elif not number_regex.match(postData['birth_day']):
            errors['birth_day'] = "Birth day should contain only numbers."
        elif not number_regex.match(postData['birth_year']):
            errors['birth_year'] = "Birth year should contain only numbers."
        
        if len(postData['playfrom']) < 1:
            errors['playfrom'] = "Please type in the year the player has started to play professional basketball."
        elif not number_regex.match(postData['playfrom']):
            errors['playfrom'] = "'Years played' should contain only numbers in the field entry."
        elif len(postData['playto']) < 1:
            errors['playto'] = "Please type in the final year the player has played. (Type 'Present' if the player is still playing professional basketball.)"
        
        if len(postData['description']) < 50:
            errors['description'] = "Player description should be 50 or more characters long." 

        return errors
    
    def coach_validate(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Name must be more than two characters long"
        
        if not number_regex.match(postData['birth_month']):
            errors['birth_month'] = "Birth month should contain only numbers."
        elif not number_regex.match(postData['birth_day']):
            errors['birth_day'] = "Birth day should contain only numbers."
        elif not number_regex.match(postData['birth_year']):
            errors['birth_year'] = "Birth year should contain only numbers."
        
        if len(postData['coachfrom']) < 1:
            errors['coachfrom'] = "Please type in the year the person started coaching."
        elif not number_regex.match(postData['coachfrom']):
            errors['coachfrom'] = "'Years coached' should contain only numbers in the field entry."
        elif len(postData['coachto']) < 1:
            errors['coachto']  = "Please type in the year the person finished coaching. (Type 'Present' if the person is still coaching a professional basketball team.)"

        if len(postData['coach_position']) < 1:
            errors['coach_position'] = "Please identify the coach's position in the team."
        if len(postData['description']) < 50:
            errors['description'] = "Coach description should be 50 or more characters long." 
        
        return errors
    
    def other_validate (self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Name must be more than two characters long"
        
        if not number_regex.match(postData['birth_month']):
            errors['birth_month'] = "Birth month should contain only numbers."
        elif not number_regex.match(postData['birth_day']):
            errors['birth_day'] = "Birth day should contain only numbers."
        elif not number_regex.match(postData['birth_year']):
            errors['birth_year'] = "Birth year should contain only numbers."
        
        if len(postData['description']) < 50:
            errors['description'] = "Description should be 50 or more characters long." 
        return errors

    def comment_validate(self, postData):
        errors = {}
        if len(postData['comment']) < 10:
            errors['comment'] = "Comment must be more than ten characters long."
        return errors
    
    def reply_validate(self, postData):
        errors = {}
        if len(postData['reply']) < 10:
            errors['reply'] = "Reply must be more than ten characters long."
        return errors
    
    def edit_validate(self, postData):  
        errors = {}
        b = User.objects.filter(email = postData['email'])

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        elif not name_regex.match(postData['first_name']):
            errors["first_name"] = "First name should contain only letters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        elif not name_regex.match(postData['last_name']):
            errors["last_name"] = "Last name should contain only letters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid e-mail address"
        elif b:
            errors["email"] = "The email already exists in our system. Please type another one."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Comment(models.Model):
    comment = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    commenter = models.ForeignKey(User, related_name = "user_comment")
    comment_likes = models.ManyToManyField(User, related_name = "liked_comment")

class Reply(models.Model):
    reply = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    replier = models.ForeignKey(User, related_name = "user_reply")
    comment = models.ForeignKey(Comment, related_name = "replied_comment")
    reply_likes = models.ManyToManyField(User, related_name = "liked_reply")

class Activity(models.Model):
    activity = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    act = models.ForeignKey(User, related_name = "active")

class Player(models.Model):
    name = models.CharField(max_length = 255)
    image = models.ImageField()
    birth_month = models.CharField(max_length = 2)
    birth_day = models.CharField(max_length = 2)
    birth_year = models.CharField(max_length = 4)
    height_foot = models.CharField(max_length = 1)
    height_inches = models.CharField(max_length = 2)
    weight = models.CharField(max_length = 3)
    position = models.CharField(max_length = 15)
    previous_teams = models.TextField(max_length = 255)
    college = models.CharField(max_length = 50)
    draft = models.CharField(max_length = 50)
    jersey = models.CharField(max_length = 3)
    playfrom = models.CharField(max_length = 4)
    playto = models.CharField(max_length = 7)
    info = models.TextField(max_length = 1000)
    description = models.TextField()
    description2 = models.TextField()
    description3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    player_creator = models.ForeignKey(User, related_name = "player_created")
    player_comments = models.ManyToManyField(Comment, related_name = "player_commented")
    player_replies = models.ManyToManyField(Comment, related_name = "player_replied")

class Coach(models.Model):
    name = models.CharField(max_length = 255)
    image = models.ImageField()
    birth_month = models.CharField(max_length = 2)
    birth_day = models.CharField(max_length = 2)
    birth_year = models.CharField(max_length = 4)
    height_foot = models.CharField(max_length = 1)
    height_inches = models.CharField(max_length = 2)
    weight = models.CharField(max_length = 3)
    position = models.CharField(max_length = 15)
    teams_played = models.TextField(max_length = 255)
    teams_coached = models.TextField(max_length = 255)
    college = models.CharField(max_length = 50)
    draft = models.CharField(max_length = 50)
    playfrom = models.CharField(max_length = 4)
    playto = models.CharField(max_length = 4)
    coachfrom = models.CharField(max_length = 4)
    coachto = models.CharField(max_length = 7)
    coach_position = models.CharField(max_length = 30)
    info = models.TextField(max_length = 1000)
    description = models.TextField()
    description2 = models.TextField()
    description3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    coach_creator = models.ForeignKey(User, related_name = "coach_created")
    coach_comments = models.ManyToManyField(Comment, related_name = "coach_commented")
    coach_replies = models.ManyToManyField(Comment, related_name = "coach_replied")

class Other(models.Model):
    name = models.CharField(max_length = 255)
    image = models.ImageField()
    birth_month = models.CharField(max_length = 2)
    birth_day = models.CharField(max_length = 2)
    birth_year = models.CharField(max_length = 4)
    height_foot = models.CharField(max_length = 1)
    height_inches = models.CharField(max_length = 2)
    weight = models.CharField(max_length = 3)
    position = models.CharField(max_length = 50)
    info = models.TextField(max_length = 1000)
    description = models.TextField()
    description2 = models.TextField()
    description3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    other_creator = models.ForeignKey(User, related_name = "other_created")
    other_comments = models.ManyToManyField(Comment, related_name = "other_commented")
    other_replies = models.ManyToManyField(Comment, related_name = "other_replied")

