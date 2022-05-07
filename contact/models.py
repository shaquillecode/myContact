from django.db import models
# Create your models here.

class Contact(models.Model):
    '''Contact Model'''
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    phone = models.CharField(max_length=20, verbose_name="Add phone" , null=True, default=None, blank=True)
    email = models.EmailField(verbose_name="Add email")
    address = models.CharField(max_length=100, verbose_name="Add Street address")

    def __str__(self):
        '''Returns Text'''
        return f"{self.first_name} phone number is {self.phone}"
