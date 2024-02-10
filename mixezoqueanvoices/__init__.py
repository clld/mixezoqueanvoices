from pyramid.config import Configurator
from clld.web.icon import MapMarker
from clld.interfaces import IMapMarker, IValueSet, IValue, ILanguage
from clldutils.svg import icon, data_url

# we must make sure custom models are known at database initialization!
from mixezoqueanvoices import models


_ = lambda s: s
_('Languages')
_('Parameters')
_('Language')
_('Parameter')


class LanguageBySubgroupMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if IValue.providedBy(ctx):
            return data_url(icon('c' + ctx.valueset.language.jsondata['color']))
        if IValueSet.providedBy(ctx):
            return data_url(icon('c' + ctx.language.jsondata['color']))
        elif ILanguage.providedBy(ctx):
            return data_url(icon('c' + ctx.jsondata['color']))

        return super(LanguageBySubgroupMapMarker, self).__call__(ctx, req)  # pragma: no cover


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_audio_plugin')
    config.registry.registerUtility(LanguageBySubgroupMapMarker(), IMapMarker)
    config.register_map('parameter', maps.ConceptMap)
    return config.make_wsgi_app()
