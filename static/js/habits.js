// static/js/habits.js
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os elementos do grid de hábitos
    const habitCells = document.querySelectorAll('[data-habit-id]');
    
    habitCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const habitId = this.dataset.habitId;
            const date = this.dataset.date;
            
            // Envia requisição AJAX para marcar/desmarcar o hábito
            fetch(`/habit/${habitId}/toggle/${date}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Atualiza a aparência do elemento
                    if (data.completed) {
                        this.classList.remove('bg-gray-200');
                        this.classList.add('bg-green-500');
                    } else {
                        this.classList.remove('bg-green-500');
                        this.classList.add('bg-gray-200');
                    }
                }
            });
        });
    });
    
    // Função para obter o cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os elementos do grid de hábitos
    const habitCells = document.querySelectorAll('.habit-cell');
    
    habitCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const habitId = this.dataset.habitId;
            const date = this.dataset.date;
            
            // Cria o objeto FormData para enviar os dados
            const formData = new FormData();
            formData.append('habit_id', habitId);
            formData.append('date', date);
            
            // Envia requisição AJAX para marcar/desmarcar o hábito
            fetch('/habits/toggle/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Atualiza a aparência do elemento
                    if (data.completed) {
                        this.classList.remove('bg-gray-200');
                        this.classList.add('bg-green-500');
                    } else {
                        this.classList.remove('bg-green-500');
                        this.classList.add('bg-gray-200');
                    }
                }
            });
        });
    });
    
    // Função para obter o cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
