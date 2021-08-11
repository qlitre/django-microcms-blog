# blog/templatetags/blog.py

from django import template
import datetime

register = template.Library()


@register.filter
def date_from_isoformat(date_string):
    """UTC時刻をyyyy-mm-ddに置き換える"""
    d = datetime.datetime.fromisoformat(date_string[:-1])
    d += datetime.timedelta(hours=9)
    return datetime.datetime.strftime(d, "%Y-%m-%d")


@register.filter
def sorted_post_tag(post_tag):
    """ポストに紐づいたタグを並び替える"""
    post_tag.sort(key=lambda x: (x['sortOrder'], x['name']))
    return post_tag
