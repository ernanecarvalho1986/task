from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'tasks/registro.html', {'erro': 'Usuário já existe!'})
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'tasks/registro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('lista_tarefas')
        return render(request, 'tasks/login.html', {'erro': 'Usuário ou senha incorretos!'})
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def lista_tarefas(request):
    tarefas = Task.objects.filter(usuario=request.user).order_by('data_limite')
    return render(request, 'tasks/lista.html', {'tarefas': tarefas})

@login_required(login_url='login')
def criar_tarefa(request):
    if request.method == 'POST':
        Task.objects.create(
            usuario     = request.user,
            titulo      = request.POST['titulo'],
            descricao   = request.POST.get('descricao', ''),
            data_limite = request.POST['data_limite'],
            whatsapp    = request.POST['whatsapp'],
        )
        return redirect('lista_tarefas')
    return render(request, 'tasks/criar.html')

@login_required(login_url='login')
def concluir_tarefa(request, pk):
    t = get_object_or_404(Task, pk=pk, usuario=request.user)
    t.delete()
    return redirect('lista_tarefas')