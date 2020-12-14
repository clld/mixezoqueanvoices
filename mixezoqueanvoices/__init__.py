from pyramid.config import Configurator


# we must make sure custom models are known at database initialization!
from mixezoqueanvoices import models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_audio_plugin')
    return config.make_wsgi_app()
