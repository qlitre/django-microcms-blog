# blog/views.py

from django.shortcuts import render
import requests
from django.conf import settings
from django.http import Http404
import math


def post_list(request, **kwargs):
    """記事一覧"""
    limit = 2
    current_page = kwargs.get('page', 1)
    offset = (int(current_page) - 1) * limit

    end_point = f'/post?limit={limit}&offset={offset}'

    tag_id = kwargs.get('tag_id', None)
    if tag_id:
        end_point += f'&filters=tag[contains]{tag_id}'

    url = getattr(settings, "BASE_URL", None)
    api_key = getattr(settings, "API_KEY", None)
    headers = {'X-API-KEY': api_key}
    res = requests.request(method='GET',
                           url=url + end_point,
                           headers=headers)

    tags_res = requests.request(method='GET',
                                url=url + '/tag',
                                headers=headers)

    tag_list = tags_res.json()['contents']
    tag_list.sort(key=lambda x: x['name'])

    total_count = res.json()['totalCount']
    num_page = math.ceil(total_count / limit)
    context = {
        'post_list': res.json()['contents'],
        'num_page': range(1, num_page + 1),
        'current_page': int(current_page),
        'last_page': num_page,
        'tag_list': tag_list,
        'tag_id': tag_id
    }

    return render(request, 'blog/index.html', context)


def post_detail(request, slug):
    """記事詳細"""
    end_point = f'/post/{slug}'
    url = getattr(settings, "BASE_URL", None)
    api_key = getattr(settings, "API_KEY", None)
    headers = {'X-API-KEY': api_key}
    res = requests.request('GET', url=url + end_point, headers=headers)

    if res.status_code != 200:
        raise Http404

    context = {
        'post': res.json()
    }

    return render(request, 'blog/post_detail.html', context)
