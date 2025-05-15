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
    
    # Obter a data atual e determinar o intervalo de datas
    today = datetime.now().date()
    
    # Data de um mês atrás para comparações
    month_ago = today - timedelta(days=30)
    
    # Determinar datas para visualização
    if view_type == 'monthly':
        date_range = [today - timedelta(days=i) for i in range(29, -1, -1)]
    elif view_type == 'compact':
        date_range = [today - timedelta(days=i) for i in range(13, -1, -1)]
    else:  # weekly
        date_range = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Preparar dados para o template
    habits_data = []
    completed_today = 0
    
    for habit in habits:
        # Obter registros para o período selecionado
        records = HabitRecord.objects.filter(
            habit=habit,
            date__in=date_range
        ).values_list('date', 'completed')
        
        # Converter para dicionário para fácil acesso
        records_dict = {date: completed for date, completed in records}
        
        # Verificar se o hábito foi completado hoje
        today_completed = records_dict.get(today, False)
        if today_completed:
            completed_today += 1
        
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
            'today_completed': today_completed
        })
    
    # Calcular estatísticas
    total_habits = len(habits)
    
    # Calcular progresso de hoje
    progress_today = 0
    if total_habits > 0:
        progress_today = int((completed_today / total_habits) * 100)
    
    # Calcular sequência atual (streak)
    current_streak = 0
    streak_date = today
    
    # Continuar calculando streak enquanto todos os hábitos do dia estiverem completos
    while True:
        if total_habits == 0:
            break
            
        # Verificar registros para esta data
        day_records = HabitRecord.objects.filter(
            habit__user=request.user,
            habit__is_archived=False,
            date=streak_date
        )
        
        if not day_records:
            break
            
        completed_count = day_records.filter(completed=True).count()
        
        if completed_count == total_habits and total_habits > 0:
            current_streak += 1
            streak_date -= timedelta(days=1)
        else:
            break
    
    # Calcular melhor sequência (consultar registros históricos)
    # Implementação simplificada - em um sistema real, você calcularia isso com base em dados históricos
    best_streak = max(current_streak, 21)  # Usando o maior entre o atual e um valor padrão
    
    # Para o heatmap na Visão Geral
    # Obtém todos os dias dos últimos 30 dias
    heatmap_dates = [today - timedelta(days=i) for i in range(29, -1, -1)]
    
    # Dicionário para armazenar a porcentagem de conclusão por dia
    daily_completion = {}
    
    for date in heatmap_dates:
        # Obter todos os registros de hábitos para esta data
        day_records = HabitRecord.objects.filter(
            habit__user=request.user,
            habit__is_archived=False,
            date=date
        )
        
        total_habits_for_day = habits.count()
        if total_habits_for_day > 0:
            completed_habits = day_records.filter(completed=True).count()
            completion_percentage = int((completed_habits / total_habits_for_day) * 100)
        else:
            completion_percentage = 0
            
        daily_completion[date.strftime('%Y-%m-%d')] = completion_percentage
    
    # Calcular taxa de sucesso (últimos 30 dias)
    days_with_records = set()
    for habit in habits:
        habit_records = HabitRecord.objects.filter(
            habit=habit,
            date__gte=today - timedelta(days=30)
        ).values_list('date', flat=True)
        days_with_records.update(habit_records)
    
    success_rate = 0
    if days_with_records:
        # Calcular quantos dias tiveram todos os hábitos completados
        successful_days = 0
        for day in days_with_records:
            day_habits = HabitRecord.objects.filter(
                habit__user=request.user,
                habit__is_archived=False,
                date=day
            )
            completed_habits = day_habits.filter(completed=True).count()
            if completed_habits == total_habits and total_habits > 0:
                successful_days += 1
        
        success_rate = int((successful_days / len(days_with_records)) * 100) if len(days_with_records) > 0 else 0
    
    # Calcular mudança na taxa de sucesso (comparando com mês anterior)
    # Implementação simplificada - em um sistema real, você calcularia isso com base em dados históricos
    success_rate_change = 12  # Valor padrão para o MVP
    
    # Calcular mudança no número de hábitos
    # Implementação simplificada - em um sistema real, você consultaria dados históricos
    habits_month_ago = Habit.objects.filter(
        user=request.user,
        created_at__lte=month_ago
    ).count()
    
    habits_change = total_habits - habits_month_ago
    
    context = {
        'habits_data': habits_data,
        'date_range': date_range,
        'view_type': view_type,
        'today': today,
        'total_habits': total_habits,
        'completed_today': completed_today,
        'progress_today': progress_today,
        'current_streak': current_streak,
        'best_streak': best_streak,
        'success_rate': success_rate,
        'success_rate_change': success_rate_change,
        'habits_change': habits_change,
        'heatmap_dates': heatmap_dates,
        'daily_completion': daily_completion,
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

@login_required
def get_counters(request):
    """Endpoint para atualizar contadores via AJAX"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        habits = Habit.objects.filter(user=request.user, is_archived=False)
        today = datetime.now().date()
        
        # Contar hábitos completados hoje
        completed_today = HabitRecord.objects.filter(
            habit__in=habits,
            date=today,
            completed=True
        ).count()
        
        total_habits = habits.count()
        progress_today = 0
        if total_habits > 0:
            progress_today = int((completed_today / total_habits) * 100)
        
        # Calcular sequência atual
        current_streak = 0
        streak_date = today
        
        while True:
            if total_habits == 0:
                break
                
            day_records = HabitRecord.objects.filter(
                habit__user=request.user,
                habit__is_archived=False,
                date=streak_date
            )
            
            if not day_records:
                break
                
            completed_count = day_records.filter(completed=True).count()
            
            if completed_count == total_habits and total_habits > 0:
                current_streak += 1
                streak_date -= timedelta(days=1)
            else:
                break
        
        # Calcular taxa de sucesso
        days_with_records = set()
        for habit in habits:
            habit_records = HabitRecord.objects.filter(
                habit=habit,
                date__gte=today - timedelta(days=30)
            ).values_list('date', flat=True)
            days_with_records.update(habit_records)
        
        success_rate = 0
        if days_with_records:
            successful_days = 0
            for day in days_with_records:
                day_habits = HabitRecord.objects.filter(
                    habit__user=request.user,
                    habit__is_archived=False,
                    date=day
                )
                completed_habits = day_habits.filter(completed=True).count()
                if completed_habits == total_habits and total_habits > 0:
                    successful_days += 1
            
            success_rate = int((successful_days / len(days_with_records)) * 100) if len(days_with_records) > 0 else 0
        
        # Para o heatmap
        heatmap_dates = [today - timedelta(days=i) for i in range(29, -1, -1)]
        daily_completion = {}
        
        for date in heatmap_dates:
            day_records = HabitRecord.objects.filter(
                habit__user=request.user,
                habit__is_archived=False,
                date=date
            )
            
            total_habits_for_day = habits.count()
            if total_habits_for_day > 0:
                completed_habits = day_records.filter(completed=True).count()
                completion_percentage = int((completed_habits / total_habits_for_day) * 100)
            else:
                completion_percentage = 0
                
            daily_completion[date.strftime('%Y-%m-%d')] = completion_percentage
        
        return JsonResponse({
            'completed_today': completed_today,
            'total_habits': total_habits,
            'progress_today': progress_today,
            'current_streak': current_streak,
            'success_rate': success_rate,
            'daily_completion': daily_completion
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
