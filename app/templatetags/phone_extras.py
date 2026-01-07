import re
from django import template

register = template.Library()

@register.filter
def wa_number(value):
    """Normalize a phone number for use in a WhatsApp wa.me link:

    - Removes all non-digit characters
    - If result is 10 digits, assumes Indian number and prefixes with '91'
    - If it starts with a single leading '0' and total len==11, strips leading '0' and prefixes '91'
    - Otherwise returns the cleaned digits as-is
    """
    if not value:
        return ''
    s = str(value)
    digits = re.sub(r"\D", "", s)

    # Common cases
    if len(digits) == 10:
        return '91' + digits
    if digits.startswith('0') and len(digits) == 11:
        return '91' + digits.lstrip('0')

    # Already includes country code or unhandled format
    return digits
