import re, itertools
import base64
from django import template

register = template.Library()


@register.filter(is_safe=True)
def bleach(text):
    #img
    text = re.sub(r'(https://forum.roderic.ca/uploads/)thumbnails/([^\s<]+)',
                  r'<a href="\1images/\2"><img src="\1thumbnails/\2"/></a>', text)
    #hyperlink
    text = re.sub(r'&lt;a href=&quot;(\S+?)&quot;&gt;(.+?)&lt;/a&gt;', r'<a href="\1">\2</a>', text)
    text = re.sub(r'(\s|>|^)(\w+://\S+?)(\s|<|$)', r'\1<a href="\2">\2</a>\3', text)

    #misc
    allowed = r'b|i|em|u|s|pre|code|spoiler|blockquote|article|header|footer|center|right|strong|figure'
    pattern = r'&lt;(/)?({})&gt;'.format(allowed)
    text = re.sub(pattern, r'<\1\2>', text)

    # footers
    for i in itertools.count(1):
        pattern = '[[{i}]]'.format(i=i)
        if text.count(pattern) != 2:
            break
        intext = '<sup><a id="{i}a" href="#{i}b">{i}</a></sup>'.format(i=i)
        infoot = '<sup><a id="{i}b" href="#{i}a">{i}</a></sup>'.format(i=i)
        text = text.replace(pattern, intext, 1)
        text = text.replace(pattern, infoot, 1)

    # quotes
    text = re.sub(r'(^|<br />)&gt;\s*([\s\S]+?)($|<br />)', r'<blockquote>\2</blockquote>', text)

    # ticks
    text = re.sub(r'`([\s\S]+?)`', r'<span class="monospace">\1</span>', text)

    return text

@register.filter(is_safe=True)
def b64encode(text):
    return base64.b64encode(bytes(text, "utf-8"))
