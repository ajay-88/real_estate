from django.db import models


# Create your models here.
class RegistrationDB(models.Model):
    UserId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    Email = models.EmailField(max_length=70, null=False,default="aa")
    Password = models.CharField(max_length=20, null=False)
    Role = models.CharField(max_length=50, null=True, blank=True)
    Account_created = models.DateTimeField(auto_now_add=True)


class PropertyDB(models.Model):
    PropertyId = models.AutoField(primary_key=True)
    Image = models.ImageField(upload_to="PropertyImage", null=True, blank=True)
    PDF = models.FileField(upload_to="PropertyPDF", null=True, blank=True)  # Add this field
    Purpose = models.CharField(max_length=20, null=True, blank=True)
    Type = models.CharField(max_length=20, null=True, blank=True)
    Title = models.CharField(max_length=50, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Price = models.IntegerField(default=0)
    Location = models.CharField(max_length=50, null=True, blank=True)
    Phone = models.PositiveBigIntegerField(null=True, blank=True)
    UserId = models.ForeignKey(RegistrationDB, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    Name=models.CharField(max_length=50)
    Gmail=models.EmailField(null=True)
    Message=models.CharField(max_length=250)