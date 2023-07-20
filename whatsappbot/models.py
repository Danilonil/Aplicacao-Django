from django.db import models


# Create your models here.
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length= 30)
    whatsapp = models.CharField(max_length=15, unique= True)
    status_conversa = models.CharField(max_length= 60)

    def __str__(self) -> str:
        return self.nome
    
