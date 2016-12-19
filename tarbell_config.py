# -*- coding: utf-8 -*-
"""
site settings
"""

from flask import Blueprint, g

blueprint = Blueprint('blog', __name__)

OG = {
    'title': 'This is my website',
    'type': 'website',
}


@blueprint.app_context_processor
def add_to_context():
    "Default context"
    context = {
        'og': OG,
    }

    return context