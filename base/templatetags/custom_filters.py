from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def time_diff(value):
    if not value:
        return ""
    
    now = timezone.now()
    end_date = value

    if isinstance(value, str):
        end_date = timezone.make_aware(datetime.strptime(value, "%Y-%m-%d"))
        
    # Time difference calculation
    delta = end_date - now
    
    # Calculate years, months, and days
    years, remainder = divmod(delta.days, 365)
    months, days = divmod(remainder, 30)

    if years > 0:
        return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
    elif months > 0:
        return f"{months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
    else:
        return f"{days} day{'s' if days > 1 else ''}"
