from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=12)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name


    def register(self): #(instance method)
        self.save()

    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email2):   #mentioning a parrameter here
        try:
            return Customer.objects.get(email=email2)
        except:
            return False























        

    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email2):   #mentioning a parrameter here
        try:
            return Customer.objects.get(email=email2)
        except:
            return False   
