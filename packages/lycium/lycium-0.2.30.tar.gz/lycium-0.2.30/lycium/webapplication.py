#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from .asynchttphandler import routes

class WebApplication(tornado.web.Application):
    """
    """
    
    def __init__(self, handlers=None, default_host=None, transforms=None, **settings):
        all_handlers = routes.routes.copy()
        if handlers:
            all_handlers.extend(handlers)
        return super().__init__(handlers=all_handlers, default_host=default_host, transforms=transforms, **settings)
