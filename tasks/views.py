from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, UserProfile
from .telegram import enviar_telegram

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        telegram_chat_id = request.POST.get('telegram_chat_id', '').strip()
        if User.objects.filter(username=username).exists():
            return render(request, 'tasks/registro.html', {'erro': 'Usuário já existe!'})
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, telegram_chat_id=telegram_chat_id)
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
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'tasks/lista.html', {'tarefas': tarefas, 'profile': profile})

@login_required(login_url='login')
def criar_tarefa(request):
    if request.method == 'POST':
        data_limite = request.POST['data_limite']
        tarefa = Task.objects.create(
            usuario     = request.user,
            titulo      = request.POST['titulo'],
            descricao   = request.POST.get('descricao', ''),
            data_limite = data_limite,
        )
        if str(data_limite) == str(date.today()):
            try:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if profile.telegram_chat_id:
                    enviar_telegram(
                        profile.telegram_chat_id,
                        f"⚠️ LEMBRETE: Tarefa '{tarefa.titulo}' vence HOJE! Conclua agora.",
                    )
            except Exception:
                pass
        return redirect('lista_tarefas')
    return render(request, 'tasks/criar.html')

@login_required(login_url='login')
def concluir_tarefa(request, pk):
    t = get_object_or_404(Task, pk=pk, usuario=request.user)
    t.delete()
    return redirect('lista_tarefas')

@login_required(login_url='login')
def perfil(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        telegram_chat_id = request.POST.get('telegram_chat_id', '').strip()
        profile.telegram_chat_id = telegram_chat_id
        profile.save()
        return render(request, 'tasks/perfil.html', {'profile': profile, 'sucesso': True})
    return render(request, 'tasks/perfil.html', {'profile': profile})
