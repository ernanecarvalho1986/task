from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def lista_tarefas(request):
    tarefas = Task.objects.all().order_by('data_limite')
    return render(request, 'tasks/lista.html', {'tarefas': tarefas})

def criar_tarefa(request):
    if request.method == 'POST':
        Task.objects.create(
            titulo      = request.POST['titulo'],
            descricao   = request.POST.get('descricao', ''),
            data_limite = request.POST['data_limite'],
            whatsapp    = request.POST['whatsapp'],
        )
        return redirect('lista_tarefas')
    return render(request, 'tasks/criar.html')

def concluir_tarefa(request, pk):
    t = get_object_or_404(Task, pk=pk)
    t.delete()
    return redirect('lista_tarefas')