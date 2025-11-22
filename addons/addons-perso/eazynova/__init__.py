# -*- coding: utf-8 -*-

from . import models
from . import wizard
from . import controllers

def post_init_hook(env):
    """Hook exécuté après l'installation du module"""
    # Configuration initiale si nécessaire
    pass
