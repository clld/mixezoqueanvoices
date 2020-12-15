from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web import datatables
from clld.web.util import concepticon
from clld.db.util import get_distinct_values
from clld.db.models import common
from clld_audio_plugin.datatables import AudioCol

from mixezoqueanvoices import models


class Languages(datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('Name')),
            Col(self,
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


class Words(datatables.Values):
    def col_defs(self):
        res = []
        if self.language:
            res.extend([
                LinkCol(self, 'gloss_en', sTitle=self.req._('English'), get_object=lambda v: v.valueset.parameter),
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
        res.extend([
            Col(self, 'name', sTitle=self.req._('Word')),
            AudioCol(self, '#')
        ])
        return res


class ConcepticonCol(Col):
    def format(self, item):
        return concepticon.link(self.dt.req, item.concepticon_id, label=item.concepticon_gloss)


class Concepts(datatables.Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('English')),
            ConcepticonCol(self, 'concepticon'),
        ]


def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
