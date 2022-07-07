from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=30)
    user_pw = models.CharField(max_length=15)

class Prescription(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_imgpath =  models.ImageField(upload_to='UploadedFiles')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class medicine(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=50)
    p_id = models.ForeignKey(Prescription, on_delete=models.CASCADE)
