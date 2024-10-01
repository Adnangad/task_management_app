from django.db import models
from django.forms.models import model_to_dict

class Users(models.Model):
    """Describes the table users"""
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    
class Tasks(models.Model):
    """describes tasks table"""
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task = models.TextField()
    status = models.BooleanField(default=False)

class DB_Manipulate:
    """Enables operations to be performed on the db"""
    def get_user(self, email):
        """Gets the user by email"""
        try:
            user = Users.objects.filter(email=email).first()
            return user
        except Exception as e:
            raise e
    def get_all_users(self):
        try:
            users = [model_to_dict(obj) for obj in Users.objects.all()]
            return users
        except Exception as e:
            raise e
