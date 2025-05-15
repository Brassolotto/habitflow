from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna um item de um dicionário pelo valor da chave"""
    return dictionary.get(key, 0)

@register.filter
def intensity_color(percentage):
    """Converte a porcentagem em um valor de opacidade para o heatmap"""
    # Normaliza a porcentagem para um valor entre 0.2 e 1.0
    # 0% = 0.2 (verde bem claro), 100% = 1.0 (verde intenso)
    return max(0.2, min(1.0, 0.2 + (percentage / 100) * 0.8))
