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

@register.filter
def color_to_rgb(hex_color):
    """Converte cor hexadecimal para RGB"""
    # Verifica se a cor é vazia
    if not hex_color:
        return "0, 0, 0"  # Retorna preto como padrão
    
    # Remove o # se existir
    hex_color = hex_color.lstrip('#')
    
    # Verifica se a string tem o tamanho correto
    if len(hex_color) != 6:
        return "0, 0, 0"  # Retorna preto como padrão
    
    try:
        # Converte para RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return f"{r}, {g}, {b}"
    except ValueError:
        # Em caso de erro na conversão
        return "0, 0, 0"  # Retorna preto como padrão

