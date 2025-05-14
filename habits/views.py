from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Habit, HabitRecord
from .forms import HabitForm
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    """Dashboard principal com visualização de hábitos"""
    # Obter o tipo de visualização da query string ou da sessão
    view_type = request.GET.get('view')
    
    if view_type:
        # Se especificado na URL, salvar na sessão
        request.session['view_type'] = view_type
    else:
        # Caso contrário, usar da sessão ou o padrão
        view_type = request.session.get('view_type', 'weekly')
    
    # Obter todos os hábitos ativos do usuário
    habits = Habit.objects.filter(user=request.user, is_archived=False)
    
    # Obter a data atual e determinar o intervalo de datas com base no tipo de visualização
    today = datetime.now().date()
    
    if view_type == 'monthly':
        # Últimos 30 dias
        date_range = [today - timedelta(days=i) for i in range(29, -1, -1)]
    elif view_type == 'compact':
        # Últimos 14 dias
        date_range = [today - timedelta(days=i) for i in range(13, -1, -1)]
    else:  # weekly
        # Últimos 7 dias
        date_range = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Preparar dados para o template
    habits_data = []
    for habit in habits:
        # Obter registros para o período selecionado
        records = HabitRecord.objects.filter(
            habit=habit,
            date__in=date_range
        ).values_list('date', 'completed')
        
        # Converter para dicionário para fácil acesso
        records_dict = {date: completed for date, completed in records}
        
        # Preparar dados do período
        period_data = []
        for date in date_range:
            completed = records_dict.get(date, False)
            period_data.append({
                'date': date,
                'completed': completed
            })
        
        habits_data.append({
            'habit': habit,
            'period_data': period_data,
            'today_completed': records_dict.get(today, False)
        })
    
    # Calcular estatísticas
    total_habits = len(habits)
    completed_today = sum(1 for h in habits_data if h['today_completed'])
    
    # Calcular progresso de hoje
    progress_today = 0
    if total_habits > 0:
        progress_today = int((completed_today / total_habits) * 100)
    
    context = {
        'habits_data': habits_data,
        'date_range': date_range,
        'view_type': view_type,
        'today': today,
        'total_habits': total_habits,
        'progress_today': progress_today
    }
    
    return render(request, 'habits/dashboard.html', context)

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
            return redirect('dashboard')
    else:
        form = HabitForm()
    
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Criar Hábito'})

@login_required
def habit_detail(request, pk):
    """Exibe detalhes de um hábito específico"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    # Obter datas para o heatmap (últimos 30 dias)
    today = datetime.now().date()
    date_range = [today - timedelta(days=i) for i in range(29, -1, -1)]
    
    # Obter registros para o período
    records = HabitRecord.objects.filter(
        habit=habit,
        date__in=date_range
    ).values_list('date', 'completed')
    
    # Converter para dicionário
    records_dict = {date: completed for date, completed in records}
    
    # Preparar dados para o heatmap
    heatmap_data = []
    for date in date_range:
        completed = records_dict.get(date, False)
        heatmap_data.append({
            'date': date,
            'completed': completed
        })
    
    # Calcular estatísticas
    total_days = len(date_range)
    completed_days = sum(1 for day in heatmap_data if day['completed'])
    completion_rate = 0
    if total_days > 0:
        completion_rate = int((completed_days / total_days) * 100)
    
    # Calcular sequência atual
    current_streak = 0
    for day in heatmap_data:
        if day['date'] <= today and day['completed']:
            current_streak += 1
        else:
            break
    
    context = {
        'habit': habit,
        'heatmap_data': heatmap_data,
        'today': today,
        'completion_rate': completion_rate,
        'current_streak': current_streak
    }
    
    return render(request, 'habits/habit_detail.html', context)

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
        return redirect('dashboard')
    
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def habit_archive(request, pk):
    """Arquiva um hábito (alternativa à exclusão)"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        habit.is_archived = True
        habit.save()
        messages.success(request, 'Hábito arquivado com sucesso!')
        return redirect('dashboard')
    
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

@login_required
def toggle_habit(request):
    """Endpoint AJAX para marcar/desmarcar hábitos"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        habit_id = request.POST.get('habit_id')
        date_str = request.POST.get('date')
        
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            record, created = HabitRecord.objects.get_or_create(
                habit=habit,
                date=date,
                defaults={'completed': True}
            )
            
            if not created:
                record.completed = not record.completed
                record.save()
            
            return JsonResponse({
                'status': 'success',
                'completed': record.completed
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
