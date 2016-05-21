import re
from django import template

register = template.Library()


@register.filter(is_safe=True)
def bleach(text):
    text = re.sub(r'&lt;img src=&quot;(.+)&quot; ?/&gt;', r'<img src="\1"/>', text)
    allowed = r'b|i|u|s|pre|code|spoiler|blockquote'
    pattern = r'&lt;(/)?({})&gt;'.format(allowed)
    bleached = re.sub(pattern, r'<\1\2>', text)
    return bleached
