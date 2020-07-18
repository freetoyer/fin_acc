from rest_framework import serializers


class ChequeSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=50)
    shop = serializers.StringRelatedField()
    summ = serializers.DecimalField(max_digits=9, decimal_places=2)
    time = serializers.DateTimeField()
    
    
class EntrySerializer(serializers.Serializer):
    cheque = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    quantity = serializers.DecimalField(max_digits=9, decimal_places=2)