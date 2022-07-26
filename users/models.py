from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 50) 
    nickname = models.CharField(max_length = 50)    
    password_hash = models.CharField(max_length = 100) 
    password_salt = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100)
    avatar_pic = models.CharField(max_length = 50)   
    status = models.IntegerField(default = 1)    #1:Normal/9:Delete
    create_at = models.DateTimeField(default = datetime.now) 
    update_at = models.DateTimeField(default = datetime.now) 

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,
        'password_hash':self.password_hash,'password_salt':self.password_salt,
        'status':self.status, 'email':self.email, 'avatar_pic':self.avatar_pic,
        'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"


class Friends(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length = 50) 
    nickname = models.CharField(max_length = 50)    
    avatar_pic = models.CharField(max_length = 50)    
    email = models.CharField(max_length = 50)    
    status = models.IntegerField(default = 1)        #1:Normal/9:Delete
    create_at = models.DateTimeField(default=datetime.now)  
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'user_id':self.user,'nickname':self.nickname,'avatar_pic':self.avatar,
        'email':self.email,'status':self.status,'username':self.username,
        'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "friends" 

