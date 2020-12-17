from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web import datatables
from clld.web.util import concepticon
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import map_marker_img
from clld.db.util import get_distinct_values
from clld.db.models import common
from clld_audio_plugin.datatables import AudioCol

from mixezoqueanvoices import models


class SubgroupCol(Col):
    def format(self, item):
        return HTML.div(map_marker_img(self.dt.req, item), ' ', HTML.span(item.subgroup))


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('Name')),
            SubgroupCol(
                self,
                'subgroup',
                sTitle=self.req._('Subgroup'),
                model_col=models.Variety.subgroup,
                choices=get_distinct_values(models.Variety.subgroup)),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class ReconstructionsCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return HTML.ul(
            *[HTML.li('{}: {}'.format(k, ', '.join(v)))
              for k, v in item.jsondata['reconstructions'].items()],
            **{'class': 'unstyled'})


class Words(datatables.Values):
    def col_defs(self):
        res = []
        if self.language:
            res.extend([
                LinkCol(
                    self,
                    'gloss_en',
                    sTitle=self.req._('English'),
                    model_col=common.Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
                Col(self,
                    'gloss_en',
                    sTitle=self.req._('Spanish'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description,
                    format=lambda i: i.valueset.parameter.description),
            ])
        elif self.parameter:
            res.extend([
                LinkCol(self, 'language', sTitle=self.req._('Language'), get_object=lambda v: v.valueset.language),
                Col(self,
                    'desc',
                    sTitle=self.req._('Location'),
                    get_object=lambda v: v.valueset.language,
                    model_col=common.Language.description,
                ),
            ])
            # FIXME: link to map!
        res.append(Col(self, 'name', sTitle=self.req._('Word')))
        if self.language:
            res.append(ReconstructionsCol(self, 'description', sTitle='Reconstruction'))
        res.append(AudioCol(self, '#'))
        return res


class ConcepticonCol(Col):
    def format(self, item):
        return concepticon.link(self.dt.req, item.concepticon_id, label=item.concepticon_gloss)


class Concepts(datatables.Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('English')),
            Col(self, 'description', sTitle='Spanish'),
            ConcepticonCol(self, 'concepticon'),
        ]


def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
