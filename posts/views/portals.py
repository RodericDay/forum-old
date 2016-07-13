import re

from django.http import HttpResponse
from django.shortcuts import render

import requests


def descape(string):
    return (string
        .replace('<p>', '\n\n')
        .replace('&#x27;', '\'')
        .replace('&quot;', '"')
        .replace('&gt;', '>')
        .replace('&#x2F;', '/')
        .replace(' rel="nofollow"', '')
    )

def hackernews(request):
    base = 'https://news.ycombinator.com/'
    path = request.path.replace('/hn/', base)
    response = requests.get(path, request.GET)
    html = response.content.decode()
    if path == base:
        us = re.findall(r'<a href="(item\?id=\d+)">\d+ comments?</a>', html)
        ts = re.findall(r'<a href=".+?" class="storylink">(.+?)</a>', html)
        context = {
            'topic_list': [
                {
                    'name': title,
                    'get_absolute_url': url,
                    'tags_as_string': 'hackernews',
                }
                for url, title in zip(us, ts)
            ]
        }
        return render(request, 'posts/topic_list.html', context)
    if path.startswith(base+'item'):
        ps = re.findall(r'<span class="c00">([\S\s]+?)<span>', html)
        ls = re.findall(r'<span class="age"><a href="(item\?id=\d+)">', html)[1:]
        context = {'topic': {'id': 999},
            'post_list': [
                {
                    'id': 999,
                    'content':  descape(content)
                                + '\n'+base+link
                }
                for content, link in zip(ps, ls)
            ]
        }
        return render(request, 'posts/post_list.html', context)
    else:
        return HttpResponse(path)
