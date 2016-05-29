import re
from django import template

register = template.Library()


@register.filter(is_safe=True)
def bleach(text):
    #img
    text = re.sub(r'&lt;img src=&quot;(.+?)&quot; ?/&gt;', r'<img src="\1"/>', text)
    #hyperlink
    text = re.sub(r'&lt;a href=&quot;(\S+?)&quot;&gt;(.+?)&lt;/a&gt;', r'<a href="\1">\2</a>', text)
    text = re.sub(r'([^"])(https?:\S+)', r'\1<a href="\2">\2</a>', text)
    #misc
    allowed = r'b|i|em|u|s|pre|code|spoiler|blockquote|article|header|footer|center|right|strong'
    pattern = r'&lt;(/)?({})&gt;'.format(allowed)
    bleached = re.sub(pattern, r'<\1\2>', text)
    return bleached
