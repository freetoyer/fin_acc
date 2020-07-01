from django.db import models


class Shop(models.Model):
    inn = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.inn


class Cheque(models.Model):
    number = models.CharField(max_length=50, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name='cheques')
    summ = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField()
        
    def __str__(self):
        return self.number


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name    
    

class Entry(models.Model):
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='entries')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='entries')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return f'Product: {self.product} Price: {self.price} Quantity: {self.quantity} Amount: {self.price*self.quantity}'


