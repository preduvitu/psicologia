from django.conf import settings
from django.db.models.fields.related import ForeignKey, OneToOneField
from django_cpf_cnpj.fields import CPFField
from django.core.validators import RegexValidator
from django.db import models
from medicos.models import Agenda
import os

class Cliente(models.Model):
    SEXO = (
        ("MAS", "Maculino"),
        ("FEM", "Feminino")
    )
    
    sexo = models.CharField(max_length=9, choices=SEXO,)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número precisa estar neste formato: \
                        '9999999999'.")

    telefone = models.CharField(verbose_name="Telefone",
                                validators=[phone_regex],
                                max_length=17, null=True, blank=True)
    cpf = CPFField(verbose_name="CPF",
                    max_length=50,
                    unique=True,)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuário', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.user.name}'
    
class Consulta(models.Model):
    agenda =  OneToOneField(Agenda, on_delete=models.CASCADE, related_name='consulta')
    cliente = ForeignKey(Cliente, on_delete=models.CASCADE, related_name='consulta')
    
    class Meta:
        unique_together = ('agenda', 'cliente')
        
    def __str__(self):
        return f'{self.agenda} - {self.cliente}'
    
class file_upload(models.Model):
    ids = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    my_file = models.FileField(upload_to='')
    
    def __str__(self):
        return self.file_name
    
class file_upload2(models.Model):
    ids = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    my_file2 = models.FileField(upload_to='')
    
    def __str__(self):
        return self.file_name
    
def get_upload_path(instance, filename):
    # Obtém o nome original do arquivo
    nome_original, extensao = os.path.splitext(filename)
    
    # Remove caracteres especiais do nome original
    nome_original = ''.join(e for e in nome_original if e.isalnum())

    # Retorna o caminho completo para o arquivo, preservando a extensão
    return f'{nome_original}{extensao}'

class MyFile(models.Model):
    arq = models.FileField(upload_to=get_upload_path)
    title = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Atribui o nome original do arquivo ao campo title antes de salvar
        self.title = os.path.basename(self.arq.name)
        
        super(MyFile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
class MyFile2(models.Model):
    arq = models.FileField(upload_to=get_upload_path)
    title = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Atribui o nome original do arquivo ao campo title antes de salvar
        self.title = os.path.basename(self.arq.name)
        
        super(MyFile2, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title