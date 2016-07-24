import re
from html import unescape

from django.http import HttpResponse
from django.shortcuts import render

import requests
from lxml import html
from lxml.etree import tostring, strip_tags


def descape(string):
    string = unescape(string)
    return (string
        .replace('<p>', '\n')
        .replace('</p>', '\n')
        .replace('<p/>', '\n')
        .replace('<span>', '')
        .replace('</span>', '')
        .replace(' rel="nofollow"', '')
    )

def stringify(node):
    string = ''.join(
        str(inner) if not isinstance(inner, html.HtmlElement)
        else tostring(inner).decode()
        for inner in node.xpath('node()')[:-1]
    )
    return descape(string)

def hackernews(request):
    base = 'https://news.ycombinator.com/'
    path = request.path.replace('/hn/', base)
    response = requests.get(path, request.GET)
    string = response.content.decode()
    page = html.fromstring(string)
    # page.make_links_absolute(base)
    titles = page.xpath('//a[@class="storylink"]/text()')
    post_nodes = page.xpath('//span[@class="comment"]/span[1]|//a[@class="storylink"]')
    authors = page.xpath('//a[@class="hnuser"]/text()')
    counts = re.findall(r'(\d+ comments?|discuss)', string)
    context = {}

    if path == base:
        urls = page.xpath('//td[@class="subtext"]/a[last()]/@href')
        context['topic_list'] = [
            {
                'name': title,
                'get_absolute_url': url,
                'tags_as_string': 'hackernews',
                'author': author,
                'post_count': 0 if count == 'discuss' else count.split()[0],
                'unseen_count': 0,
            }
            for title, url, author, count
            in zip(titles, urls, authors, counts)
        ]
        return render(request, 'posts/topic_list.html', context)

    if path.startswith(base+'item'):
        urls = page.xpath('//span[@class="age"]/a/@href')
        context['post_list'] = [
            {
                'id': 999,
                'get_absolute_url': url,
                'content': stringify(node),
                'author': author,
            }
            for node, author, url
            in zip(post_nodes, authors, urls)
        ]
        context['post_list'][0]['content'] += '\n' + response.url
        context['topic'] = {'id': 999}  # shouldn't be necessary
        return render(request, 'posts/post_list.html', context)
