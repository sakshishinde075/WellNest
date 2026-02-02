from django import template

register = template.Library()

@register.filter
def get_risk_level_display(risk_level):
    """Get display text for risk level."""
    risk_levels = {
        'low': 'Low Risk',
        'moderate': 'Moderate Risk',
        'high': 'High Risk'
    }
    return risk_levels.get(risk_level, 'Unknown')

@register.filter
def get_risk_level_color(risk_level):
    """Get Tailwind CSS color class for risk level."""
    colors = {
        'low': 'text-green-600 bg-green-100',
        'moderate': 'text-yellow-600 bg-yellow-100',
        'high': 'text-red-600 bg-red-100'
    }
    return colors.get(risk_level, 'text-gray-600 bg-gray-100')
