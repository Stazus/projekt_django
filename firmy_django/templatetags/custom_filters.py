from django import template

register = template.Library()

@register.filter
def format_pln(value):
    """
    Formatuje kwotę na polski format PLN:
    np. 82383209.59 → 82 383 209,59
    """
    try:
        # usuń spacje i zamień przecinek na kropkę, jeśli jest w liczbie
        num = float(str(value).replace(" ", "").replace(",", "."))
        # formatowanie z separatorem tysięcy jako spacja i przecinkiem dziesiętnym
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
    except (ValueError, TypeError):
        # jeśli nie da się przekonwertować na float, zwróć jako string
        return str(value)
