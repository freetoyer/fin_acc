from django.db import models


class Cheque(models.Model):
    number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField()
        
    def __str__(self):
        return self.number


class Shop(models.Model):
    cheque = models.OneToOneField(Cheque, on_delete=models.DO_NOTHING)
    inn = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.inn


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name    
    

class Entry(models.Model):
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='cheque_entries')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_entries')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return f'Product: {self.product} Price: {self.price} Quantity: {self.quantity} Amount: {self.amount}'


