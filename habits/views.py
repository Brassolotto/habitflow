from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit, HabitRecord
from .forms import HabitForm

@login_required
def habit_list(request):
    """Lista todos os hábitos ativos do usuário"""
    habits = Habit.objects.filter(user=request.user, is_archived=False)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    """Cria um novo hábito"""
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Hábito criado com sucesso!')
            return redirect('habit_list')
    else:
        form = HabitForm()
    
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Criar Hábito'})

@login_required
def habit_detail(request, pk):
    """Exibe detalhes de um hábito específico"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    records = habit.records.all()
    
    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'records': records
    })

@login_required
def habit_update(request, pk):
    """Atualiza um hábito existente"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hábito atualizado com sucesso!')
            return redirect('habit_detail', pk=habit.pk)
    else:
        form = HabitForm(instance=habit)
    
    return render(request, 'habits/habit_form.html', {
        'form': form,
        'title': 'Editar Hábito',
        'habit': habit
    })

@login_required
def habit_delete(request, pk):
    """Exclui um hábito"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Hábito excluído com sucesso!')
        return redirect('habit_list')
    
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def habit_archive(request, pk):
    """Arquiva um hábito (alternativa à exclusão)"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        habit.is_archived = True
        habit.save()
        messages.success(request, 'Hábito arquivado com sucesso!')
        return redirect('habit_list')
    
    return render(request, 'habits/habit_confirm_archive.html', {'habit': habit})

@login_required
def toggle_habit_record(request, habit_id, date):
    """Marca/desmarca um hábito em uma data específica"""
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    
    record, created = HabitRecord.objects.get_or_create(
        habit=habit,
        date=date,
        defaults={'completed': True}
    )
    
    if not created:
        record.completed = not record.completed
        record.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'completed': record.completed})
    
    return redirect('habit_detail', pk=habit.pk)
