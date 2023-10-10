from django.db import models


# Create your models here.



#-clientes------------------------------------------------------------------


class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.TextField()
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return self.rua

class Contato(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length= 30)
    whatsapp = models.CharField(max_length=15, unique= True)
    endereco = models.OneToOneField(Endereco, on_delete= models.SET_NULL, null= True, blank= True)
    status_conversa = models.TextField()

    def __str__(self) -> str:
        return self.nome
    


#-cardapio------------------------------------------------------------------

# class Produto(models.Model):
#     id = models.AutoField(primary_key=True)
#     categoria = models.CharField(max_length= 30)

#     def __str__(self) -> str:
#         return self.categoria
    

# class Pizza(models.Model):
#     id = models.AutoField(primary_key=True)
#     nome = models.CharField(max_length= 30)
#     descrição = models.TextField(null=True, blank=True)
#     valor = models.DecimalField(max_digits=6, decimal_places=2)
#     produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.nome
    
#-conversa------------------------------------------------------------------

# class Pedido(models.Model):
#     id = models.AutoField(primary_key=True)
#     #cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     pedido = models.TextField(null=True, blank=True)
    