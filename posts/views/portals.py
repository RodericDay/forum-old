import re

from django.http import HttpResponse
from django.shortcuts import render

import requests
from lxml import html
from lxml.etree import tostring, strip_tags


def descape(string):
    return (string
        .replace('<p>', '\n')
        .replace('</p>', '\n')
        .replace('<p/>', '\n')
        .replace('<span>', '')
        .replace('</span>', '')
        .replace('&#x27;', '\'')
        .replace('&#8217;', '\'')
        .replace('&amp;', '&')
        .replace('&quot;', '"')
        .replace('&gt;', '>')
        .replace('&#x2F;', '/')
        .replace(' rel="nofollow"', '')
    )

def hackernews(request):
    base = 'https://news.ycombinator.com/'
    path = request.path.replace('/hn/', base)
    response = requests.get(path, request.GET)
    page = html.fromstring(response.content.decode())
    # page.make_links_absolute(base)
    titles = page.xpath('//a[@class="storylink"]/text()')
    urls = page.xpath('//td[@class="subtext"]/a[last()]/@href')
    post_nodes = page.xpath('//span[@class="comment"]/span[1]')

    if path == base:
        context = {'topic_list': []}
        for title, url in zip(titles, urls):
            topic = {
                'name': title,
                'get_absolute_url': url,
                'tags_as_string': 'hackernews'
            }
            context['topic_list'].append(topic)
        return render(request, 'posts/topic_list.html', context)

    if path.startswith(base+'item'):
        context = {'post_list': [{'id':999, 'content': response.url}]}
        context['topic'] = {'id': 999}  # shouldn't be necessary
        for node in post_nodes:
            content = []
            for inner in node.xpath('node()')[:-1]:
                try:
                    string = tostring(inner).decode()
                except:
                    string = str(inner)
                content.append(string)

            post = {
                'id': 999,
                'content': descape(''.join(content)),
            }
            context['post_list'].append(post)
        return render(request, 'posts/post_list.html', context)
