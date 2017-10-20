# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from cdnjs import CDNStorage


register = template.Library()
cdn_manager = CDNStorage()


@register.simple_tag(name='cdn')
def cdn_static(name, filename=None):
    """
    Returns static file url
    :param name: Is the repository name.
    :param filename:
    :return:
    """
    return cdn_manager.get(name, filename)
