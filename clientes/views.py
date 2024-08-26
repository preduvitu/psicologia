from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente, Consulta, MyFile, MyFile2
from django.http import HttpResponse
from PIL import Image
from django.urls import reverse
from django.views import View
import os 
from django.conf import settings
from datetime import date
from .models import file_upload
from .models import file_upload2
from django.core.files.storage import default_storage

from django.shortcuts import get_object_or_404, redirect, render

def show_file(request):
    all_files = MyFile.objects.all()
    file_data = [{'name': file.arq.name, 'link': file.arq.url} for file in all_files]

    context = {'file_data': file_data}
    return render(request, 'media.html', context)


def show_file2(request):
    all_files = MyFile2.objects.all()
    file_data = [{'name': file.arq.name, 'link': file.arq.url} for file in all_files]

    context = {'file_data': file_data}
    return render(request, 'media.html', context)



class ClienteCreateView(LoginRequiredMixin ,CreateView):
    
    model = Cliente
    template_name = 'clientes/cadastro.html'
    fields = ['sexo', 'telefone', 'cpf']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ClienteUpdateView(LoginRequiredMixin, UpdateView):

    model = Cliente
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/update_user.html'
    fields = ['sexo', 'telefone', 'cpf']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        user = self.request.user
        try:
            return Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            return None
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        

class ConsultaCreateView(LoginRequiredMixin, CreateView):

    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('clientes:consulta_list')
    
    def form_valid(self, form):
        try:
            form.instance.cliente = Cliente.objects.get(user=self.request.user)
            form.save()
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in e.args[0]:
                messages.warning(self.request, 'Você não pode marcar esta consulta')
                return HttpResponseRedirect(reverse_lazy('clientes:consulta_create'))
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Complete seu cadastro')
            return HttpResponseRedirect(reverse_lazy('clientes:cliente_cadastro'))
        messages.info(self.request, 'Consulta marcada com sucesso!')
        return HttpResponseRedirect(reverse_lazy('clientes:consulta_list'))
    
class ConsultaUpdateView(LoginRequiredMixin, UpdateView):

    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('medicos:Consulta_lista')
    
    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        return super().form_valid(form)
    
class ConsultaDeleteView(LoginRequiredMixin, DeleteView):
    model = Consulta
    success_url = reverse_lazy('clientes:consulta_list')
    template_name = 'form_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Consulta excluída com sucesso!")
        return reverse_lazy('clientes:consulta_list')


class ConsultaListView(LoginRequiredMixin, ListView):
    
    login_url = 'accounts:login'
    template_name = 'clientes/consulta_list.html'

    def get_queryset(self):
        user=self.request.user
        try:
            cliente = Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Crie uma Consulta')
            return None
        try:
            consultas = Consulta.objects.filter(cliente=cliente).order_by('-pk')
        except Consulta.DoesNotExist:
            messages.warning(self.request, 'Crie uma Consulta')
            return None
        return consultas

class DetalhesListView(ListView):

    model = Consulta
    template_name = 'detalhes.html'
    fields = ['agenda']

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_queryset(self):
        user=self.request.user
        try:
            cliente = Cliente.objects.get(user=user)
            consultas = Consulta.objects.filter(cliente=cliente).order_by('-pk')
            return consultas
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Crie uma Consulta')
            return Consulta.objects.none() 

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("my_file")
        mf = MyFile(title="minha_imagem", arq=file)
        mf.save()
        print(file)

        consulta_id = self.kwargs['pk']
        url = reverse('clientes:detalhes', kwargs={'pk': consulta_id})
        return redirect(url)
    
class PainelView(View):
    def post(self, request, *args, **kwargs):
        mf = MyFile(title=request.FILES.get("my_file").name, arq=request.FILES.get("my_file"))
        mf.save()

        return HttpResponse('Arquivo de prontuário recebido com sucesso.')

cliente_cadastro = ClienteCreateView.as_view()
cliente_atualizar = ClienteUpdateView.as_view()
consulta_lista = ConsultaListView.as_view()
consulta_cadastro = ConsultaCreateView.as_view()
consulta_atualizar = ConsultaUpdateView.as_view()
consulta_excluir = ConsultaDeleteView.as_view()
detalhes = DetalhesListView.as_view()
painel = PainelView.as_view()
