# -*- coding: utf-8 -*-

from . import models
from . import wizard
from . import controllers


def post_init_hook(cr, registry):
    """Hook post-installation du module EAZYNOVA Core"""
    import logging
    _logger = logging.getLogger(__name__)
    _logger.info("EAZYNOVA Core module installé avec succès")
