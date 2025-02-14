from django import template
from datetime import datetime, date
from django.utils import timezone
from datetime import datetime as dt

register = template.Library()

@register.filter
def time_diff(value):
    if not value:
        return ""

    # Ensure value is a datetime object
    now = timezone.now()

    # If value is a date object but not a datetime, convert it to datetime
    if isinstance(value, date) and not isinstance(value, datetime):
        # Convert to datetime if it's a date object
        value = datetime.combine(value, datetime.min.time())

    # Make sure both now and value are timezone aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    if timezone.is_naive(now):
        now = timezone.make_aware(now, timezone.get_current_timezone())

    # Calculate the time difference
    delta = value - now

    # Calculate years, months, and days
    years, remainder = divmod(delta.days, 365)
    months, days = divmod(remainder, 30)

    if years > 0:
        return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
    elif months > 0:
        return f"{months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
    else:
        return f"{days} day{'s' if days > 1 else ''}"
