# -*- coding: utf-8 -*-

import os
import json
import requests
import feedparser


github_token = os.getenv('github_token')


def get_latest_package():
    packages = []
    pypi_feed = feedparser.parse('https://pypi.python.org/pypi?%3Aaction=rss')

    for i in pypi_feed['entries']:
        packages.append(i['title'].replace(' ', '=='))

    return packages


def create_issue(title, body, labels):
    global github_token
    url = 'https://api.github.com/repos/fate0/projects/issues'
    data = {
        'title': title,
        'body': body,
        'labels': labels
    }
    headers = {
        'Authorization': 'token %s' % github_token
    }

    print(title)
    print(body)

    try:
        requests.post(
            url=url,
            headers=headers,
            data='```\n%s\n```' % json.dumps(data)
        )
    except:
        pass


if __name__ == '__main__':
    packages = get_latest_package()
    for p_name in packages:
        os.system('python fakepip.py install %s' % p_name)

    for p_name in packages:
        if not os.path.exists('/tmp/%s.txt' % p_name):
            continue

        content = open('/tmp/%s.txt' % p_name).read()
        create_issue(p_name, content, ['pypi', 'evil'])
