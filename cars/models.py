from django.db import models

#Criando a tabela Brand e Car, onde a tabela Car possui uma chave estrangeira para a tabela Brand
class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class Car(models.Model):
    id = models.AutoField(primary_key=True) #coluna criada apenas como meio academico, pois o django cria automaticamente uma coluna id para cada model
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand')
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    plate = models.CharField( blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='cars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model


#Criando a tabela CarInventory, que irá armazenar o total de carros e o valor total dos carros cadastrados no sistema
class CarInventory(models.Model):
    cars_count = models.IntegerField(blank=True, null=True)
    cars_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} carros, valor total: {self.cars_value}'
    


